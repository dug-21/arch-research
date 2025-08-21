# WebForms Security Testing Checklist

## Overview
This checklist provides comprehensive security testing strategies for ASP.NET WebForms applications, addressing common vulnerabilities and security concerns specific to the WebForms architecture.

## Security Testing Categories

### 1. Input Validation and Sanitization

#### SQL Injection Testing
```csharp
[TestClass]
public class SqlInjectionTests
{
    private CustomerService _customerService;
    private Mock<ICustomerRepository> _mockRepository;
    
    [TestInitialize]
    public void Setup()
    {
        _mockRepository = new Mock<ICustomerRepository>();
        _customerService = new CustomerService(_mockRepository.Object);
    }
    
    [TestMethod]
    public void CustomerSearch_SqlInjectionAttempt_HandledSafely()
    {
        // Arrange - Common SQL injection payloads
        var sqlInjectionPayloads = new[]
        {
            "'; DROP TABLE Customers; --",
            "' OR 1=1 --",
            "' UNION SELECT * FROM Users --",
            "'; INSERT INTO Customers VALUES ('hack', 'hacker'); --",
            "' OR 'a'='a",
            "admin'--",
            "admin' #",
            "admin'/*",
            "' or 1=1#",
            "' or 1=1--",
            "') or '1'='1--",
            "') or ('1'='1--"
        };
        
        foreach (var payload in sqlInjectionPayloads)
        {
            try
            {
                // Act
                var request = new SearchCustomerRequest { Email = payload };
                var result = _customerService.SearchCustomers(request);
                
                // Assert - Should handle gracefully without SQL execution
                Assert.IsNotNull(result, $"Service should return result for payload: {payload}");
                Assert.IsFalse(result.IsSuccess, "Should reject malicious input");
                
                // Verify repository wasn't called with malicious input
                _mockRepository.Verify(r => r.SearchByEmail(payload), Times.Never, 
                    $"Repository should not be called with SQL injection payload: {payload}");
            }
            catch (ArgumentException)
            {
                // Expected - input validation should catch this
                Assert.IsTrue(true, "Input validation correctly rejected malicious input");
            }
            catch (SqlException)
            {
                Assert.Fail($"SQL injection vulnerability detected with payload: {payload}");
            }
        }
    }
    
    [TestMethod]
    public void CustomerRepository_ParameterizedQueries_PreventsSqlInjection()
    {
        // Test direct repository with real database connection
        var repository = new CustomerRepository(TestConnectionString);
        var maliciousEmail = "'; DROP TABLE Customers; --";
        
        try
        {
            // This should use parameterized queries internally
            var results = repository.SearchByEmail(maliciousEmail);
            
            // Should return empty results, not cause SQL error
            Assert.IsNotNull(results);
            Assert.AreEqual(0, results.Count);
            
            // Verify table still exists by running a simple query
            var allCustomers = repository.GetAll();
            Assert.IsNotNull(allCustomers, "Table should still exist after injection attempt");
        }
        catch (SqlException ex)
        {
            Assert.Fail($"SQL injection vulnerability detected: {ex.Message}");
        }
    }
}
```

#### Cross-Site Scripting (XSS) Testing
```csharp
[TestClass]
public class XssTests
{
    [TestMethod]
    public void CustomerForm_XssPayloads_OutputEncoded()
    {
        var xssPayloads = new[]
        {
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<div onclick=alert('XSS')>Click me</div>",
            "';alert('XSS');//",
            "\"><script>alert('XSS')</script>",
            "<script>document.cookie='stolen'</script>"
        };
        
        foreach (var payload in xssPayloads)
        {
            // Test input sanitization
            var sanitizedInput = HtmlSanitizer.Sanitize(payload);
            
            Assert.IsFalse(sanitizedInput.Contains("<script>"), 
                $"Script tags should be removed from: {payload}");
            Assert.IsFalse(sanitizedInput.Contains("javascript:"), 
                $"JavaScript protocols should be removed from: {payload}");
            Assert.IsFalse(sanitizedInput.Contains("onerror"), 
                $"Event handlers should be removed from: {payload}");
            
            // Test output encoding
            var encodedOutput = HttpUtility.HtmlEncode(payload);
            Assert.IsFalse(encodedOutput.Contains("<script>"), 
                $"Script tags should be encoded in: {payload}");
            Assert.IsTrue(encodedOutput.Contains("&lt;") || encodedOutput.Contains("&gt;"), 
                $"HTML should be encoded in: {payload}");
        }
    }
    
    [TestMethod]
    public void CustomerGridView_UserContent_SafelyRendered()
    {
        // Test that user-generated content in GridView is properly encoded
        var customers = new List<Customer>
        {
            new Customer { Name = "<script>alert('XSS')</script>", Email = "test@example.com" },
            new Customer { Name = "<img src=x onerror=alert('XSS')>", Email = "test2@example.com" },
            new Customer { Name = "Normal Name", Email = "<script>alert('XSS')</script>@example.com" }
        };
        
        foreach (var customer in customers)
        {
            // Simulate GridView rendering
            var renderedName = RenderGridViewCell(customer.Name);
            var renderedEmail = RenderGridViewCell(customer.Email);
            
            Assert.IsFalse(renderedName.Contains("<script>"), 
                "GridView should encode script tags in names");
            Assert.IsFalse(renderedEmail.Contains("<script>"), 
                "GridView should encode script tags in emails");
            
            // Verify proper HTML encoding
            if (customer.Name.Contains("<"))
            {
                Assert.IsTrue(renderedName.Contains("&lt;"), 
                    "GridView should HTML encode special characters");
            }
        }
    }
    
    private string RenderGridViewCell(string content)
    {
        // Simulate proper GridView rendering with encoding
        return HttpUtility.HtmlEncode(content);
    }
}
```

### 2. Authentication and Authorization Testing

#### Authentication Security Tests
```csharp
[TestClass]
public class AuthenticationSecurityTests
{
    private IWebDriver _driver;
    private string _baseUrl = "http://localhost:8080";
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void LoginForm_BruteForceAttempts_ImplementsProtection()
    {
        _driver.Navigate().GoToUrl($"{_baseUrl}/Login.aspx");
        
        var attempts = 0;
        var maxAttempts = 5;
        var lockedOut = false;
        
        for (int i = 1; i <= maxAttempts + 2; i++)
        {
            // Attempt login with wrong credentials
            _driver.FindElement(By.Id("txtUsername")).Clear();
            _driver.FindElement(By.Id("txtUsername")).SendKeys("testuser");
            
            _driver.FindElement(By.Id("txtPassword")).Clear();
            _driver.FindElement(By.Id("txtPassword")).SendKeys($"wrongpassword{i}");
            
            _driver.FindElement(By.Id("btnLogin")).Click();
            
            // Check for lockout message
            try
            {
                var errorMessage = _driver.FindElement(By.Id("lblError")).Text;
                if (errorMessage.Contains("account locked") || errorMessage.Contains("too many attempts"))
                {
                    lockedOut = true;
                    attempts = i;
                    break;
                }
            }
            catch (NoSuchElementException)
            {
                // No error message found, continue
            }
        }
        
        Assert.IsTrue(lockedOut, "Account should be locked after multiple failed attempts");
        Assert.IsTrue(attempts <= maxAttempts, 
            $"Account should be locked within {maxAttempts} attempts, was locked after {attempts}");
    }
    
    [TestMethod]
    public void SecurePages_UnauthenticatedAccess_RedirectsToLogin()
    {
        var securePages = new[]
        {
            "/CustomerManagement.aspx",
            "/AdminPanel.aspx",
            "/Reports.aspx",
            "/UserProfile.aspx"
        };
        
        foreach (var page in securePages)
        {
            _driver.Navigate().GoToUrl($"{_baseUrl}{page}");
            
            // Should redirect to login page
            var currentUrl = _driver.Url.ToLower();
            Assert.IsTrue(currentUrl.Contains("login.aspx"), 
                $"Unauthenticated access to {page} should redirect to login");
        }
    }
    
    [TestMethod]
    public void PasswordField_SecurityAttributes_Implemented()
    {
        _driver.Navigate().GoToUrl($"{_baseUrl}/Login.aspx");
        
        var passwordField = _driver.FindElement(By.Id("txtPassword"));
        
        // Check password field attributes
        var fieldType = passwordField.GetAttribute("type");
        var autocomplete = passwordField.GetAttribute("autocomplete");
        
        Assert.AreEqual("password", fieldType, "Password field should have type='password'");
        Assert.AreEqual("current-password", autocomplete, 
            "Password field should have appropriate autocomplete attribute");
    }
}
```

#### Authorization and Role-Based Access Control
```csharp
[TestClass]
public class AuthorizationTests
{
    [TestMethod]
    public void AdminPages_RegularUser_AccessDenied()
    {
        // Test with different user roles
        var userRoles = new[]
        {
            new { Role = "User", ShouldAccess = false },
            new { Role = "Manager", ShouldAccess = false },
            new { Role = "Admin", ShouldAccess = true }
        };
        
        var adminPages = new[]
        {
            "/AdminPanel.aspx",
            "/UserManagement.aspx",
            "/SystemSettings.aspx"
        };
        
        foreach (var userRole in userRoles)
        {
            foreach (var page in adminPages)
            {
                var hasAccess = TestPageAccess(page, userRole.Role);
                
                if (userRole.ShouldAccess)
                {
                    Assert.IsTrue(hasAccess, 
                        $"{userRole.Role} should have access to {page}");
                }
                else
                {
                    Assert.IsFalse(hasAccess, 
                        $"{userRole.Role} should NOT have access to {page}");
                }
            }
        }
    }
    
    private bool TestPageAccess(string page, string role)
    {
        // Simulate role-based access check
        var authService = new AuthorizationService();
        var user = new TestUser { Role = role };
        
        return authService.CanAccessPage(user, page);
    }
    
    [TestMethod]
    public void CustomerData_UserIsolation_EnforcesDataSeparation()
    {
        var customerService = new CustomerService();
        
        // Test that users can only access their own data
        var user1 = new TestUser { Id = 1, Role = "User" };
        var user2 = new TestUser { Id = 2, Role = "User" };
        var admin = new TestUser { Id = 3, Role = "Admin" };
        
        // User 1 should only see their customers
        var user1Customers = customerService.GetCustomersForUser(user1);
        Assert.IsTrue(user1Customers.All(c => c.OwnerId == user1.Id), 
            "User should only see their own customers");
        
        // User 2 should only see their customers
        var user2Customers = customerService.GetCustomersForUser(user2);
        Assert.IsTrue(user2Customers.All(c => c.OwnerId == user2.Id), 
            "User should only see their own customers");
        
        // Admin should see all customers
        var adminCustomers = customerService.GetCustomersForUser(admin);
        Assert.IsTrue(adminCustomers.Count >= user1Customers.Count + user2Customers.Count, 
            "Admin should see all customers");
    }
}
```

### 3. Session and State Management Security

#### Session Security Tests
```csharp
[TestClass]
public class SessionSecurityTests
{
    [TestMethod]
    public void SessionConfiguration_SecuritySettings_Implemented()
    {
        // Test session security configuration
        var sessionConfig = GetSessionConfiguration();
        
        Assert.IsTrue(sessionConfig.CookieTimeout <= TimeSpan.FromMinutes(30), 
            "Session timeout should be reasonable");
        Assert.IsTrue(sessionConfig.CookieHttpOnly, 
            "Session cookies should be HTTP-only");
        Assert.IsTrue(sessionConfig.CookieSecure, 
            "Session cookies should be secure in production");
        Assert.IsTrue(sessionConfig.RegenerateIdOnLogin, 
            "Session ID should be regenerated on login");
    }
    
    [TestMethod]
    public void SessionData_SensitiveInformation_NotStored()
    {
        var session = new TestSession();
        
        // Attempt to store sensitive data in session
        var sensitiveData = new[]
        {
            "password123",
            "4111111111111111", // Credit card number
            "123-45-6789", // SSN
            "secret_key_12345"
        };
        
        foreach (var data in sensitiveData)
        {
            try
            {
                session.Store("test_key", data);
                
                // Check if sensitive data detection works
                var validator = new SessionDataValidator();
                var isValid = validator.ValidateStoredData(session);
                
                Assert.IsFalse(isValid, 
                    $"Session should not allow storage of sensitive data: {data}");
            }
            catch (SecurityException)
            {
                // Expected - sensitive data should be rejected
                Assert.IsTrue(true, "Sensitive data correctly rejected");
            }
        }
    }
    
    [TestMethod]
    public void SessionFixation_LoginProcess_RegeneratesSessionId()
    {
        var sessionManager = new SessionManager();
        
        // Get initial session ID
        var initialSessionId = sessionManager.GetSessionId();
        
        // Simulate login
        var loginResult = sessionManager.Login("testuser", "password123");
        
        // Get session ID after login
        var postLoginSessionId = sessionManager.GetSessionId();
        
        Assert.IsTrue(loginResult.IsSuccess, "Login should succeed");
        Assert.AreNotEqual(initialSessionId, postLoginSessionId, 
            "Session ID should change after successful login");
    }
}
```

### 4. ViewState and Control State Security

#### ViewState Security Tests
```csharp
[TestClass]
public class ViewStateSecurityTests
{
    [TestMethod]
    public void ViewState_Tampering_DetectedAndHandled()
    {
        var originalViewState = GenerateValidViewState();
        var tamperedViewState = TamperWithViewState(originalViewState);
        
        try
        {
            var page = new TestPage();
            page.LoadViewState(tamperedViewState);
            
            Assert.Fail("Tampered ViewState should be rejected");
        }
        catch (ViewStateException)
        {
            // Expected - tampering should be detected
            Assert.IsTrue(true, "ViewState tampering correctly detected");
        }
        catch (HttpException ex) when (ex.Message.Contains("ViewState"))
        {
            // Expected - ASP.NET should reject invalid ViewState
            Assert.IsTrue(true, "ViewState tampering correctly detected by ASP.NET");
        }
    }
    
    [TestMethod]
    public void ViewState_Encryption_EnabledForSensitiveData()
    {
        // Test that ViewState encryption is enabled
        var pageConfig = GetPageConfiguration();
        
        Assert.IsTrue(pageConfig.ViewStateEncryptionMode != ViewStateEncryptionMode.Never, 
            "ViewState encryption should be enabled");
        
        // Test that sensitive controls require encryption
        var sensitiveControls = new[] { "txtCreditCard", "txtSSN", "txtPassword" };
        
        foreach (var controlId in sensitiveControls)
        {
            var control = CreateControl(controlId);
            Assert.IsTrue(control.ViewStateMode == ViewStateMode.Enabled && 
                         pageConfig.RequiresViewStateEncryption(control), 
                $"Control {controlId} should require ViewState encryption");
        }
    }
    
    [TestMethod]
    public void ViewState_SizeLimit_EnforcedForSecurity()
    {
        var maxViewStateSize = 4 * 1024 * 1024; // 4MB limit
        
        var largeViewState = GenerateLargeViewState(maxViewStateSize + 1000);
        
        try
        {
            var page = new TestPage();
            page.LoadViewState(largeViewState);
            
            Assert.Fail("Oversized ViewState should be rejected");
        }
        catch (ArgumentException ex) when (ex.Message.Contains("ViewState"))
        {
            Assert.IsTrue(true, "Large ViewState correctly rejected");
        }
    }
    
    private string GenerateValidViewState()
    {
        // Generate a valid ViewState for testing
        var data = new Dictionary<string, object>
        {
            {"control1", "value1"},
            {"control2", "value2"}
        };
        
        return Convert.ToBase64String(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(data)));
    }
    
    private string TamperWithViewState(string viewState)
    {
        // Modify the ViewState to simulate tampering
        var bytes = Convert.FromBase64String(viewState);
        bytes[0] = (byte)(bytes[0] ^ 0xFF); // Flip some bits
        return Convert.ToBase64String(bytes);
    }
    
    private string GenerateLargeViewState(int size)
    {
        var largeData = new string('A', size);
        return Convert.ToBase64String(Encoding.UTF8.GetBytes(largeData));
    }
}
```

### 5. File Upload Security

#### File Upload Security Tests
```csharp
[TestClass]
public class FileUploadSecurityTests
{
    [TestMethod]
    public void FileUpload_MaliciousFiles_Rejected()
    {
        var maliciousFiles = new[]
        {
            new { Name = "virus.exe", Content = "MZ...", ShouldReject = true },
            new { Name = "script.aspx", Content = "<%@ Page", ShouldReject = true },
            new { Name = "shell.php", Content = "<?php system", ShouldReject = true },
            new { Name = "normal.txt", Content = "Normal content", ShouldReject = false },
            new { Name = "document.pdf", Content = "%PDF-1.4", ShouldReject = false }
        };
        
        var fileUploadService = new FileUploadService();
        
        foreach (var file in maliciousFiles)
        {
            var fileBytes = Encoding.UTF8.GetBytes(file.Content);
            var result = fileUploadService.ValidateFile(file.Name, fileBytes);
            
            if (file.ShouldReject)
            {
                Assert.IsFalse(result.IsValid, 
                    $"Malicious file {file.Name} should be rejected");
                Assert.IsTrue(result.Errors.Any(), 
                    $"Rejection of {file.Name} should include error message");
            }
            else
            {
                Assert.IsTrue(result.IsValid, 
                    $"Safe file {file.Name} should be accepted");
            }
        }
    }
    
    [TestMethod]
    public void FileUpload_SizeLimit_Enforced()
    {
        var fileUploadService = new FileUploadService();
        var maxSize = 10 * 1024 * 1024; // 10MB
        
        // Test file within limit
        var smallFile = new byte[1024]; // 1KB
        var smallResult = fileUploadService.ValidateFile("small.txt", smallFile);
        Assert.IsTrue(smallResult.IsValid, "Small file should be accepted");
        
        // Test file exceeding limit
        var largeFile = new byte[maxSize + 1000];
        var largeResult = fileUploadService.ValidateFile("large.txt", largeFile);
        Assert.IsFalse(largeResult.IsValid, "Large file should be rejected");
        Assert.IsTrue(largeResult.Errors.Any(e => e.Contains("size")), 
            "Should include size limit error");
    }
    
    [TestMethod]
    public void FileUpload_PathTraversal_Prevented()
    {
        var pathTraversalAttempts = new[]
        {
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc//passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd"
        };
        
        var fileUploadService = new FileUploadService();
        
        foreach (var maliciousPath in pathTraversalAttempts)
        {
            var result = fileUploadService.ValidateFileName(maliciousPath);
            
            Assert.IsFalse(result.IsValid, 
                $"Path traversal attempt should be rejected: {maliciousPath}");
            Assert.IsTrue(result.Errors.Any(e => e.Contains("invalid") || e.Contains("path")), 
                $"Should include path validation error for: {maliciousPath}");
        }
    }
}
```

### 6. Configuration and Infrastructure Security

#### Configuration Security Tests
```csharp
[TestClass]
public class ConfigurationSecurityTests
{
    [TestMethod]
    public void WebConfig_SecuritySettings_Configured()
    {
        var config = GetWebConfiguration();
        
        // Check security-related configuration
        Assert.IsFalse(config.DebugMode, 
            "Debug mode should be disabled in production");
        Assert.IsFalse(config.TraceEnabled, 
            "Trace should be disabled in production");
        Assert.IsFalse(config.CustomErrorsOff, 
            "Custom errors should be enabled");
        
        // Check HTTPS enforcement
        Assert.IsTrue(config.RequireSSL, 
            "HTTPS should be required");
        Assert.IsTrue(config.CookieRequireSSL, 
            "Cookies should require SSL");
        
        // Check request validation
        Assert.IsTrue(config.RequestValidationEnabled, 
            "Request validation should be enabled");
        Assert.IsTrue(config.ValidateRequestEnabled, 
            "Request validation should be enabled");
    }
    
    [TestMethod]
    public void ConnectionStrings_Encryption_Implemented()
    {
        var connectionStrings = ConfigurationManager.ConnectionStrings;
        
        foreach (ConnectionStringSettings connString in connectionStrings)
        {
            if (connString.Name != "LocalSqlServer")
            {
                // Check that connection strings don't contain plain text passwords
                Assert.IsFalse(connString.ConnectionString.Contains("password="), 
                    $"Connection string {connString.Name} should not contain plain text password");
                
                // Should use integrated security or encrypted passwords
                Assert.IsTrue(
                    connString.ConnectionString.Contains("Integrated Security=true") ||
                    connString.ConnectionString.Contains("Trusted_Connection=true") ||
                    IsEncryptedConnectionString(connString.ConnectionString), 
                    $"Connection string {connString.Name} should use secure authentication");
            }
        }
    }
    
    private bool IsEncryptedConnectionString(string connectionString)
    {
        // Check if connection string appears to be encrypted
        return !connectionString.Contains("=") || 
               connectionString.Length < 50 || // Too short to be real connection string
               Regex.IsMatch(connectionString, @"^[A-Za-z0-9+/=]+$"); // Base64 pattern
    }
    
    [TestMethod]
    public void ErrorHandling_InformationDisclosure_Prevented()
    {
        var errorHandler = new GlobalErrorHandler();
        
        var sensitiveExceptions = new[]
        {
            new SqlException("Login failed for user 'sa'"),
            new DirectoryServiceException("LDAP connection failed"),
            new FileNotFoundException("Config file not found at C:\\SecretPath\\"),
            new UnauthorizedAccessException("Access denied to C:\\Windows\\System32\\")
        };
        
        foreach (var exception in sensitiveExceptions)
        {
            var errorResponse = errorHandler.HandleException(exception);
            
            Assert.IsFalse(errorResponse.Message.Contains("sa"), 
                "Error should not disclose database usernames");
            Assert.IsFalse(errorResponse.Message.Contains("C:\\"), 
                "Error should not disclose file paths");
            Assert.IsFalse(errorResponse.Message.Contains("LDAP"), 
                "Error should not disclose infrastructure details");
            
            Assert.IsTrue(errorResponse.Message.Contains("error occurred") || 
                         errorResponse.Message.Contains("please try again"), 
                "Error should provide generic message");
        }
    }
}
```

### 7. Security Headers and HTTPS

#### Security Headers Tests
```csharp
[TestClass]
public class SecurityHeadersTests
{
    private HttpClient _httpClient;
    
    [TestInitialize]
    public void Setup()
    {
        _httpClient = new HttpClient();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _httpClient?.Dispose();
    }
    
    [TestMethod]
    public async Task SecurityHeaders_Required_Present()
    {
        var response = await _httpClient.GetAsync("https://localhost:8080/CustomerForm.aspx");
        
        var requiredHeaders = new Dictionary<string, string[]>
        {
            {"X-Frame-Options", new[] {"DENY", "SAMEORIGIN"}},
            {"X-Content-Type-Options", new[] {"nosniff"}},
            {"X-XSS-Protection", new[] {"1; mode=block", "0"}},
            {"Strict-Transport-Security", new[] {"max-age="}},
            {"Content-Security-Policy", new[] {"default-src", "script-src"}}
        };
        
        foreach (var header in requiredHeaders)
        {
            Assert.IsTrue(response.Headers.Contains(header.Key) || 
                         response.Content.Headers.Contains(header.Key), 
                $"Required security header {header.Key} is missing");
            
            var headerValue = GetHeaderValue(response, header.Key);
            var isValidValue = header.Value.Any(validValue => 
                headerValue.Contains(validValue, StringComparison.OrdinalIgnoreCase));
            
            Assert.IsTrue(isValidValue, 
                $"Security header {header.Key} has invalid value: {headerValue}");
        }
    }
    
    [TestMethod]
    public async Task HTTPS_Redirect_Enforced()
    {
        try
        {
            var httpResponse = await _httpClient.GetAsync("http://localhost:8080/CustomerForm.aspx");
            
            // Should redirect to HTTPS or be blocked
            Assert.IsTrue(httpResponse.StatusCode == HttpStatusCode.Redirect || 
                         httpResponse.StatusCode == HttpStatusCode.MovedPermanently ||
                         httpResponse.StatusCode == HttpStatusCode.BadRequest, 
                "HTTP requests should be redirected to HTTPS or blocked");
            
            if (httpResponse.StatusCode == HttpStatusCode.Redirect || 
                httpResponse.StatusCode == HttpStatusCode.MovedPermanently)
            {
                var location = httpResponse.Headers.Location?.ToString();
                Assert.IsTrue(location?.StartsWith("https://"), 
                    "Redirect should be to HTTPS URL");
            }
        }
        catch (HttpRequestException)
        {
            // Expected if HTTP is completely blocked
            Assert.IsTrue(true, "HTTP requests appropriately blocked");
        }
    }
    
    private string GetHeaderValue(HttpResponseMessage response, string headerName)
    {
        if (response.Headers.TryGetValues(headerName, out var values))
            return string.Join(", ", values);
        
        if (response.Content.Headers.TryGetValues(headerName, out var contentValues))
            return string.Join(", ", contentValues);
        
        return string.Empty;
    }
}
```

## Security Testing Automation

### 1. Automated Security Scanning
```csharp
[TestClass]
public class AutomatedSecurityTests
{
    [TestMethod]
    public void SecurityScan_OWASP_Top10_Vulnerabilities()
    {
        var securityScanner = new OWASPSecurityScanner();
        var targetUrl = "http://localhost:8080";
        
        var scanResults = securityScanner.ScanApplication(targetUrl);
        
        // Check for OWASP Top 10 vulnerabilities
        var criticalVulnerabilities = scanResults.Vulnerabilities
            .Where(v => v.Severity == VulnerabilitySeverity.Critical)
            .ToList();
        
        Assert.AreEqual(0, criticalVulnerabilities.Count, 
            $"Found {criticalVulnerabilities.Count} critical vulnerabilities: " +
            string.Join(", ", criticalVulnerabilities.Select(v => v.Name)));
        
        // Log all findings
        foreach (var vulnerability in scanResults.Vulnerabilities)
        {
            TestContext.WriteLine($"{vulnerability.Severity}: {vulnerability.Name} - {vulnerability.Description}");
        }
    }
    
    [TestMethod]
    public void PenetrationTest_CommonAttacks_Defended()
    {
        var penetrationTester = new AutomatedPenTester();
        var testSuite = new[]
        {
            PenTestType.SqlInjection,
            PenTestType.XssAttack,
            PenTestType.CsrfAttack,
            PenTestType.DirectoryTraversal,
            PenTestType.AuthenticationBypass,
            PenTestType.SessionHijacking
        };
        
        var results = new List<PenTestResult>();
        
        foreach (var testType in testSuite)
        {
            var result = penetrationTester.RunTest(testType, "http://localhost:8080");
            results.Add(result);
            
            Assert.IsFalse(result.Successful, 
                $"Penetration test {testType} should not succeed - vulnerability detected");
        }
        
        // Generate security report
        GenerateSecurityReport(results);
    }
    
    private void GenerateSecurityReport(List<PenTestResult> results)
    {
        var report = new StringBuilder();
        report.AppendLine("# Security Test Report");
        report.AppendLine($"Generated: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss} UTC");
        report.AppendLine();
        
        foreach (var result in results)
        {
            report.AppendLine($"## {result.TestType}");
            report.AppendLine($"Status: {(result.Successful ? "❌ VULNERABLE" : "✅ PROTECTED")}");
            report.AppendLine($"Details: {result.Details}");
            report.AppendLine();
        }
        
        File.WriteAllText("security-test-report.md", report.ToString());
    }
    
    public TestContext TestContext { get; set; }
}
```

## Security Testing Best Practices

### 1. Test Environment Security
- Use dedicated test environments that mirror production
- Implement secure test data management
- Regular security updates for test infrastructure
- Isolated network environments for security testing

### 2. Continuous Security Testing
- Integrate security tests into CI/CD pipeline
- Automated vulnerability scanning on every build
- Regular penetration testing schedules
- Security regression testing

### 3. Security Test Coverage
- Input validation for all entry points
- Authentication and authorization mechanisms
- Session management security
- Data protection and encryption
- Error handling and information disclosure
- Configuration security

### 4. Security Test Documentation
- Document all security test cases
- Maintain security testing checklists
- Record and track security findings
- Regular security test reviews and updates

### 5. Compliance and Standards
- Follow OWASP testing guidelines
- Implement industry-specific security requirements
- Regular compliance audits
- Security testing training for team members

This comprehensive security testing checklist ensures WebForms applications are protected against common vulnerabilities and maintain strong security posture throughout the development lifecycle.