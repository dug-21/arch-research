# WebForms UI Testing Strategies

## Overview
This guide provides comprehensive strategies for testing the user interface of ASP.NET WebForms applications, addressing the unique challenges of the WebForms architecture and postback model.

## UI Testing Challenges in WebForms

### 1. Complex Control Hierarchy
WebForms generates complex HTML with dynamic IDs, nested controls, and ViewState that make element identification challenging.

### 2. Postback Model
Full page postbacks can cause timing issues and state management complications in automated tests.

### 3. ViewState Dependencies
Heavy reliance on ViewState affects form submission and control state management.

### 4. Server Control Rendering
Server controls generate different HTML output based on browser capabilities and configurations.

### 5. Event-Driven Architecture
Complex event handling and page lifecycle make interaction testing more challenging.

## UI Testing Frameworks and Tools

### 1. Selenium WebDriver (Recommended)
Selenium provides robust browser automation capabilities for WebForms testing.

**Basic Setup:**
```csharp
[TestClass]
public class WebFormsUITests
{
    private IWebDriver _driver;
    private string _baseUrl = "http://localhost:8080";
    
    [TestInitialize]
    public void Setup()
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless"); // For CI/CD environments
        options.AddArgument("--no-sandbox");
        options.AddArgument("--disable-dev-shm-usage");
        
        _driver = new ChromeDriver(options);
        _driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
        _driver.Manage().Window.Maximize();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
        _driver?.Dispose();
    }
}
```

### 2. Playwright (Modern Alternative)
Playwright offers faster execution and better debugging capabilities.

**Playwright Setup:**
```csharp
[TestClass]
public class PlaywrightWebFormsTests
{
    private IPlaywright _playwright;
    private IBrowser _browser;
    private IPage _page;
    
    [TestInitialize]
    public async Task Setup()
    {
        _playwright = await Playwright.CreateAsync();
        _browser = await _playwright.Chromium.LaunchAsync(new BrowserTypeLaunchOptions
        {
            Headless = true
        });
        _page = await _browser.NewPageAsync();
    }
    
    [TestCleanup]
    public async Task Cleanup()
    {
        await _browser?.CloseAsync();
        _playwright?.Dispose();
    }
}
```

## Page Object Model Implementation

### 1. Base Page Object
```csharp
public abstract class BasePageObject
{
    protected readonly IWebDriver Driver;
    protected readonly WebDriverWait Wait;
    
    protected BasePageObject(IWebDriver driver)
    {
        Driver = driver;
        Wait = new WebDriverWait(driver, TimeSpan.FromSeconds(30));
    }
    
    protected IWebElement FindElement(By locator)
    {
        return Wait.Until(driver => driver.FindElement(locator));
    }
    
    protected IList<IWebElement> FindElements(By locator)
    {
        Wait.Until(driver => driver.FindElements(locator).Count > 0);
        return Driver.FindElements(locator);
    }
    
    protected void WaitForPostback()
    {
        // Wait for postback to complete by checking for specific element or page state
        Wait.Until(driver => 
            ((IJavaScriptExecutor)driver).ExecuteScript("return document.readyState").Equals("complete"));
        
        // Additional wait for UpdatePanels if using AJAX
        Wait.Until(driver => 
            ((IJavaScriptExecutor)driver).ExecuteScript("return typeof(Sys) !== 'undefined' && Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() === false"));
    }
    
    protected string GetControlClientId(string controlId)
    {
        // WebForms generates client IDs, find the actual rendered ID
        var script = $"return document.querySelector('[id$=\"{controlId}\"]').id;";
        return (string)((IJavaScriptExecutor)Driver).ExecuteScript(script);
    }
}
```

### 2. Customer Form Page Object
```csharp
public class CustomerFormPage : BasePageObject
{
    // Locators using partial ID matching for WebForms controls
    private readonly By _emailTextBox = By.CssSelector("input[id$='txtEmail']");
    private readonly By _nameTextBox = By.CssSelector("input[id$='txtName']");
    private readonly By _phoneTextBox = By.CssSelector("input[id$='txtPhone']");
    private readonly By _saveButton = By.CssSelector("input[id$='btnSave']");
    private readonly By _cancelButton = By.CssSelector("input[id$='btnCancel']");
    private readonly By _messageLabel = By.CssSelector("span[id$='lblMessage']");
    private readonly By _validationSummary = By.CssSelector("div[id$='ValidationSummary1']");
    
    public CustomerFormPage(IWebDriver driver) : base(driver) { }
    
    public CustomerFormPage NavigateTo()
    {
        Driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        WaitForPageLoad();
        return this;
    }
    
    public CustomerFormPage EnterEmail(string email)
    {
        var emailField = FindElement(_emailTextBox);
        emailField.Clear();
        emailField.SendKeys(email);
        return this;
    }
    
    public CustomerFormPage EnterName(string name)
    {
        var nameField = FindElement(_nameTextBox);
        nameField.Clear();
        nameField.SendKeys(name);
        return this;
    }
    
    public CustomerFormPage EnterPhone(string phone)
    {
        var phoneField = FindElement(_phoneTextBox);
        phoneField.Clear();
        phoneField.SendKeys(phone);
        return this;
    }
    
    public CustomerFormPage ClickSave()
    {
        FindElement(_saveButton).Click();
        WaitForPostback();
        return this;
    }
    
    public CustomerFormPage ClickCancel()
    {
        FindElement(_cancelButton).Click();
        WaitForPostback();
        return this;
    }
    
    public string GetMessage()
    {
        try
        {
            return FindElement(_messageLabel).Text;
        }
        catch (NoSuchElementException)
        {
            return string.Empty;
        }
    }
    
    public List<string> GetValidationErrors()
    {
        try
        {
            var summary = FindElement(_validationSummary);
            return summary.FindElements(By.TagName("li"))
                         .Select(li => li.Text)
                         .ToList();
        }
        catch (NoSuchElementException)
        {
            return new List<string>();
        }
    }
    
    public bool IsFormEmpty()
    {
        return string.IsNullOrEmpty(GetEmailValue()) &&
               string.IsNullOrEmpty(GetNameValue()) &&
               string.IsNullOrEmpty(GetPhoneValue());
    }
    
    public string GetEmailValue() => FindElement(_emailTextBox).GetAttribute("value");
    public string GetNameValue() => FindElement(_nameTextBox).GetAttribute("value");
    public string GetPhoneValue() => FindElement(_phoneTextBox).GetAttribute("value");
    
    private void WaitForPageLoad()
    {
        Wait.Until(driver => FindElement(_emailTextBox).Displayed);
    }
}
```

## Comprehensive UI Test Suite

### 1. Form Submission Tests
```csharp
[TestClass]
public class CustomerFormUITests : WebFormsUITests
{
    private CustomerFormPage _customerForm;
    
    [TestInitialize]
    public void TestSetup()
    {
        base.Setup();
        _customerForm = new CustomerFormPage(_driver);
    }
    
    [TestMethod]
    public void SubmitForm_ValidData_ShowsSuccessMessage()
    {
        // Arrange
        var testData = new
        {
            Email = "john.doe@example.com",
            Name = "John Doe",
            Phone = "555-123-4567"
        };
        
        // Act
        _customerForm
            .NavigateTo()
            .EnterEmail(testData.Email)
            .EnterName(testData.Name)
            .EnterPhone(testData.Phone)
            .ClickSave();
        
        // Assert
        var message = _customerForm.GetMessage();
        Assert.IsTrue(message.Contains("Customer saved successfully"), 
            $"Expected success message, but got: '{message}'");
        
        // Verify form is cleared after successful submission
        Assert.IsTrue(_customerForm.IsFormEmpty(), "Form should be cleared after successful save");
    }
    
    [TestMethod]
    public void SubmitForm_EmptyEmail_ShowsValidationError()
    {
        // Act
        _customerForm
            .NavigateTo()
            .EnterName("John Doe")
            .EnterPhone("555-123-4567")
            .ClickSave();
        
        // Assert
        var errors = _customerForm.GetValidationErrors();
        Assert.IsTrue(errors.Any(e => e.Contains("Email is required")), 
            $"Expected email validation error. Actual errors: {string.Join(", ", errors)}");
    }
    
    [TestMethod]
    public void SubmitForm_InvalidEmailFormat_ShowsValidationError()
    {
        // Act
        _customerForm
            .NavigateTo()
            .EnterEmail("invalid-email-format")
            .EnterName("John Doe")
            .ClickSave();
        
        // Assert
        var errors = _customerForm.GetValidationErrors();
        Assert.IsTrue(errors.Any(e => e.Contains("Invalid email format")), 
            $"Expected email format validation error. Actual errors: {string.Join(", ", errors)}");
    }
    
    [TestMethod]
    public void ClickCancel_WithFormData_ClearsForm()
    {
        // Arrange
        _customerForm
            .NavigateTo()
            .EnterEmail("test@example.com")
            .EnterName("Test User");
        
        // Act
        _customerForm.ClickCancel();
        
        // Assert
        Assert.IsTrue(_customerForm.IsFormEmpty(), "Form should be cleared after cancel");
    }
}
```

### 2. Client-Side Validation Tests
```csharp
[TestMethod]
public void EmailField_InvalidFormat_ShowsClientSideValidation()
{
    // Navigate to form
    _customerForm.NavigateTo();
    
    // Enter invalid email and tab away to trigger client validation
    _customerForm.EnterEmail("invalid-email");
    
    // Tab to next field to trigger validation
    var nameField = _driver.FindElement(By.CssSelector("input[id$='txtName']"));
    nameField.Click();
    
    // Check for client-side validation message
    var isValid = (bool)((IJavaScriptExecutor)_driver).ExecuteScript(
        "return document.querySelector('input[id$=\"txtEmail\"]').validity.valid;");
    
    Assert.IsFalse(isValid, "Client-side validation should mark email as invalid");
}

[TestMethod]
public void RequiredFields_Empty_PreventFormSubmission()
{
    // Navigate and try to submit empty form
    _customerForm.NavigateTo().ClickSave();
    
    // Check if form prevented submission using JavaScript validation
    var currentUrl = _driver.Url;
    Assert.IsTrue(currentUrl.Contains("CustomerForm.aspx"), 
        "Form submission should be prevented by client-side validation");
    
    // Check for validation summary display
    var errors = _customerForm.GetValidationErrors();
    Assert.IsTrue(errors.Count > 0, "Should show validation errors for required fields");
}
```

### 3. AJAX and UpdatePanel Testing
```csharp
public class AjaxCustomerFormPage : BasePageObject
{
    private readonly By _updatePanel = By.CssSelector("div[id$='UpdatePanel1']");
    private readonly By _loadingIndicator = By.CssSelector("div[id$='LoadingPanel']");
    
    public AjaxCustomerFormPage(IWebDriver driver) : base(driver) { }
    
    public AjaxCustomerFormPage ClickSaveAsync()
    {
        FindElement(_saveButton).Click();
        WaitForAjaxPostback();
        return this;
    }
    
    private void WaitForAjaxPostback()
    {
        // Wait for loading indicator to appear
        Wait.Until(driver => FindElement(_loadingIndicator).Displayed);
        
        // Wait for loading indicator to disappear
        Wait.Until(driver => !FindElement(_loadingIndicator).Displayed);
        
        // Wait for UpdatePanel to be updated
        Wait.Until(driver => 
            ((IJavaScriptExecutor)driver).ExecuteScript(
                "return typeof(Sys) !== 'undefined' && " +
                "Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() === false"));
    }
}

[TestMethod]
public void AjaxFormSubmission_ValidData_UpdatesWithoutFullPostback()
{
    var ajaxForm = new AjaxCustomerFormPage(_driver);
    
    // Record initial page elements to verify no full postback occurred
    var initialTitle = _driver.Title;
    var initialUrl = _driver.Url;
    
    // Submit form via AJAX
    ajaxForm
        .NavigateTo()
        .EnterEmail("ajax@example.com")
        .EnterName("Ajax User")
        .ClickSaveAsync();
    
    // Verify no full page reload occurred
    Assert.AreEqual(initialTitle, _driver.Title, "Page title should not change during AJAX postback");
    Assert.AreEqual(initialUrl, _driver.Url, "URL should not change during AJAX postback");
    
    // Verify success message appears
    var message = ajaxForm.GetMessage();
    Assert.IsTrue(message.Contains("Customer saved successfully"), 
        "Success message should appear after AJAX save");
}
```

## Advanced UI Testing Scenarios

### 1. File Upload Testing
```csharp
public class FileUploadPage : BasePageObject
{
    private readonly By _fileUpload = By.CssSelector("input[id$='FileUpload1']");
    private readonly By _uploadButton = By.CssSelector("input[id$='btnUpload']");
    private readonly By _statusLabel = By.CssSelector("span[id$='lblStatus']");
    
    public FileUploadPage(IWebDriver driver) : base(driver) { }
    
    public FileUploadPage SelectFile(string filePath)
    {
        FindElement(_fileUpload).SendKeys(filePath);
        return this;
    }
    
    public FileUploadPage ClickUpload()
    {
        FindElement(_uploadButton).Click();
        WaitForPostback();
        return this;
    }
    
    public string GetStatus() => FindElement(_statusLabel).Text;
}

[TestMethod]
public void FileUpload_ValidFile_ShowsSuccessMessage()
{
    var uploadPage = new FileUploadPage(_driver);
    var testFilePath = Path.Combine(TestContext.TestDir, "TestFiles", "sample.pdf");
    
    // Create test file if it doesn't exist
    if (!File.Exists(testFilePath))
    {
        Directory.CreateDirectory(Path.GetDirectoryName(testFilePath));
        File.WriteAllText(testFilePath, "Sample PDF content");
    }
    
    uploadPage
        .NavigateTo()
        .SelectFile(testFilePath)
        .ClickUpload();
    
    var status = uploadPage.GetStatus();
    Assert.IsTrue(status.Contains("File uploaded successfully"), 
        $"Expected success message, got: {status}");
}
```

### 2. GridView Testing
```csharp
public class CustomerGridPage : BasePageObject
{
    private readonly By _gridView = By.CssSelector("table[id$='GridView1']");
    private readonly By _gridRows = By.CssSelector("table[id$='GridView1'] tr:not(.header)");
    private readonly By _pager = By.CssSelector("table[id$='GridView1'] tr.pager");
    
    public CustomerGridPage(IWebDriver driver) : base(driver) { }
    
    public List<CustomerGridRow> GetCustomers()
    {
        var rows = FindElements(_gridRows);
        return rows.Select(row => new CustomerGridRow(row)).ToList();
    }
    
    public CustomerGridPage ClickEdit(int rowIndex)
    {
        var editButton = _driver.FindElement(
            By.CssSelector($"table[id$='GridView1'] tr:nth-child({rowIndex + 2}) input[value='Edit']"));
        editButton.Click();
        WaitForPostback();
        return this;
    }
    
    public CustomerGridPage ClickDelete(int rowIndex)
    {
        var deleteButton = _driver.FindElement(
            By.CssSelector($"table[id$='GridView1'] tr:nth-child({rowIndex + 2}) input[value='Delete']"));
        deleteButton.Click();
        
        // Handle confirmation dialog
        var alert = Wait.Until(driver => driver.SwitchTo().Alert());
        alert.Accept();
        WaitForPostback();
        return this;
    }
    
    public CustomerGridPage GoToPage(int pageNumber)
    {
        var pageLink = FindElement(By.LinkText(pageNumber.ToString()));
        pageLink.Click();
        WaitForPostback();
        return this;
    }
}

public class CustomerGridRow
{
    private readonly IWebElement _row;
    
    public CustomerGridRow(IWebElement row)
    {
        _row = row;
    }
    
    public string Email => _row.FindElement(By.CssSelector("td:nth-child(1)")).Text;
    public string Name => _row.FindElement(By.CssSelector("td:nth-child(2)")).Text;
    public string Phone => _row.FindElement(By.CssSelector("td:nth-child(3)")).Text;
}

[TestMethod]
public void GridView_DeleteCustomer_RemovesFromGrid()
{
    var gridPage = new CustomerGridPage(_driver);
    
    gridPage.NavigateTo();
    var initialCustomers = gridPage.GetCustomers();
    var initialCount = initialCustomers.Count;
    
    // Delete first customer
    gridPage.ClickDelete(0);
    
    var updatedCustomers = gridPage.GetCustomers();
    Assert.AreEqual(initialCount - 1, updatedCustomers.Count, 
        "Customer count should decrease by 1 after deletion");
}
```

### 3. Cross-Browser Testing
```csharp
[TestClass]
public class CrossBrowserTests
{
    private readonly Dictionary<string, Func<IWebDriver>> _browsers = new()
    {
        {"Chrome", () => new ChromeDriver()},
        {"Firefox", () => new FirefoxDriver()},
        {"Edge", () => new EdgeDriver()}
    };
    
    [TestMethod]
    [DynamicData(nameof(GetBrowsers), DynamicDataSourceType.Method)]
    public void CustomerForm_SubmitValidData_WorksInAllBrowsers(string browserName, Func<IWebDriver> browserFactory)
    {
        using var driver = browserFactory();
        driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
        
        var customerForm = new CustomerFormPage(driver);
        
        customerForm
            .NavigateTo()
            .EnterEmail("test@example.com")
            .EnterName("Test User")
            .ClickSave();
        
        var message = customerForm.GetMessage();
        Assert.IsTrue(message.Contains("Customer saved successfully"), 
            $"Form submission failed in {browserName}");
    }
    
    public static IEnumerable<object[]> GetBrowsers()
    {
        yield return new object[] { "Chrome", new Func<IWebDriver>(() => new ChromeDriver()) };
        yield return new object[] { "Firefox", new Func<IWebDriver>(() => new FirefoxDriver()) };
        yield return new object[] { "Edge", new Func<IWebDriver>(() => new EdgeDriver()) };
    }
}
```

## Performance and Load Testing for UI

### 1. Page Load Performance
```csharp
[TestMethod]
public void CustomerForm_PageLoad_CompletesWithinAcceptableTime()
{
    var stopwatch = Stopwatch.StartNew();
    
    _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
    
    // Wait for page to be fully loaded
    var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(30));
    wait.Until(driver => ((IJavaScriptExecutor)driver)
        .ExecuteScript("return document.readyState").Equals("complete"));
    
    stopwatch.Stop();
    
    Assert.IsTrue(stopwatch.ElapsedMilliseconds < 3000, 
        $"Page load took too long: {stopwatch.ElapsedMilliseconds}ms");
}

[TestMethod]
public void CustomerForm_FormSubmission_CompletesWithinAcceptableTime()
{
    _customerForm.NavigateTo()
        .EnterEmail("perf@example.com")
        .EnterName("Performance Test");
    
    var stopwatch = Stopwatch.StartNew();
    _customerForm.ClickSave();
    stopwatch.Stop();
    
    Assert.IsTrue(stopwatch.ElapsedMilliseconds < 2000, 
        $"Form submission took too long: {stopwatch.ElapsedMilliseconds}ms");
}
```

### 2. Memory Usage Testing
```csharp
[TestMethod]
public void GridView_LargeDataset_DoesNotCauseMemoryIssues()
{
    var gridPage = new CustomerGridPage(_driver);
    gridPage.NavigateTo();
    
    // Navigate through multiple pages to test memory usage
    for (int page = 1; page <= 10; page++)
    {
        gridPage.GoToPage(page);
        
        // Verify page loads successfully
        var customers = gridPage.GetCustomers();
        Assert.IsTrue(customers.Count > 0, $"Page {page} should contain customers");
        
        // Check for JavaScript errors
        var jsErrors = ((IJavaScriptExecutor)_driver).ExecuteScript(
            "return window.jsErrors || [];") as IEnumerable<object>;
        Assert.IsFalse(jsErrors?.Any() == true, "No JavaScript errors should occur during navigation");
    }
}
```

## Accessibility Testing

### 1. Basic Accessibility Checks
```csharp
[TestMethod]
public void CustomerForm_AccessibilityCompliance_MeetsBasicRequirements()
{
    _customerForm.NavigateTo();
    
    // Check for proper form labels
    var emailLabel = _driver.FindElement(By.XPath("//label[@for[contains(., 'txtEmail')]]"));
    Assert.IsNotNull(emailLabel, "Email field should have associated label");
    
    var nameLabel = _driver.FindElement(By.XPath("//label[@for[contains(., 'txtName')]]"));
    Assert.IsNotNull(nameLabel, "Name field should have associated label");
    
    // Check for proper heading structure
    var headings = _driver.FindElements(By.TagName("h1"));
    Assert.IsTrue(headings.Count > 0, "Page should have at least one H1 heading");
    
    // Check for alt text on images
    var images = _driver.FindElements(By.TagName("img"));
    foreach (var img in images)
    {
        var altText = img.GetAttribute("alt");
        Assert.IsNotNull(altText, "All images should have alt text");
    }
}

[TestMethod]
public void CustomerForm_KeyboardNavigation_IsFullyAccessible()
{
    _customerForm.NavigateTo();
    
    var emailField = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
    emailField.Click();
    
    // Navigate through form using Tab key
    emailField.SendKeys("test@example.com");
    emailField.SendKeys(Keys.Tab);
    
    var nameField = _driver.SwitchTo().ActiveElement();
    Assert.IsTrue(nameField.GetAttribute("id").Contains("txtName"), 
        "Tab should move focus to name field");
    
    nameField.SendKeys("Test User");
    nameField.SendKeys(Keys.Tab);
    
    var phoneField = _driver.SwitchTo().ActiveElement();
    Assert.IsTrue(phoneField.GetAttribute("id").Contains("txtPhone"), 
        "Tab should move focus to phone field");
}
```

## Test Data Management

### 1. Test Data Setup and Cleanup
```csharp
[TestClass]
public class CustomerFormTestsWithData : WebFormsUITests
{
    private DatabaseHelper _dbHelper;
    
    [TestInitialize]
    public void TestSetup()
    {
        base.Setup();
        _dbHelper = new DatabaseHelper(ConfigurationManager.ConnectionStrings["TestDB"].ConnectionString);
        _dbHelper.CleanDatabase();
        _dbHelper.SeedTestData();
    }
    
    [TestCleanup]
    public void TestCleanup()
    {
        _dbHelper?.CleanDatabase();
        base.Cleanup();
    }
    
    [TestMethod]
    public void CustomerForm_DuplicateEmail_ShowsErrorMessage()
    {
        // Arrange - test data already seeded with existing customer
        var existingEmail = "existing@example.com";
        
        // Act
        _customerForm
            .NavigateTo()
            .EnterEmail(existingEmail)
            .EnterName("New Customer")
            .ClickSave();
        
        // Assert
        var message = _customerForm.GetMessage();
        Assert.IsTrue(message.Contains("Email already exists"), 
            $"Expected duplicate email error, got: {message}");
    }
}
```

### 2. Dynamic Test Data Generation
```csharp
public static class TestDataGenerator
{
    private static readonly Random Random = new Random();
    private static readonly string[] FirstNames = { "John", "Jane", "Bob", "Alice", "Charlie", "Diana" };
    private static readonly string[] LastNames = { "Doe", "Smith", "Johnson", "Brown", "Wilson", "Garcia" };
    private static readonly string[] Domains = { "example.com", "test.org", "sample.net" };
    
    public static CustomerTestData GenerateCustomer()
    {
        var firstName = FirstNames[Random.Next(FirstNames.Length)];
        var lastName = LastNames[Random.Next(LastNames.Length)];
        var domain = Domains[Random.Next(Domains.Length)];
        
        return new CustomerTestData
        {
            Email = $"{firstName.ToLower()}.{lastName.ToLower()}@{domain}",
            Name = $"{firstName} {lastName}",
            Phone = GeneratePhoneNumber()
        };
    }
    
    private static string GeneratePhoneNumber()
    {
        return $"555-{Random.Next(100, 999)}-{Random.Next(1000, 9999)}";
    }
}

public class CustomerTestData
{
    public string Email { get; set; }
    public string Name { get; set; }
    public string Phone { get; set; }
}
```

## Continuous Integration Integration

### 1. CI/CD Pipeline Configuration
```yaml
# Azure DevOps Pipeline
stages:
- stage: UITests
  jobs:
  - job: RunUITests
    pool:
      vmImage: 'windows-latest'
    steps:
    - task: UseDotNet@2
      inputs:
        packageType: 'sdk'
        version: '6.0.x'
    
    - task: NuGetToolInstaller@1
    
    - task: NuGetCommand@2
      inputs:
        restoreSolution: '**/*.sln'
    
    - task: VSBuild@1
      inputs:
        solution: '**/*.sln'
        configuration: 'Release'
    
    - task: IISWebAppDeploymentOnMachineGroup@0
      inputs:
        webSiteName: 'TestSite'
        package: '$(System.DefaultWorkingDirectory)/**/*.zip'
    
    - task: VSTest@2
      inputs:
        testSelector: 'testAssemblies'
        testAssemblyVer2: |
          **/*UI*Tests.dll
          !**/*TestAdapter.dll
          !**/obj/**
        searchFolder: '$(System.DefaultWorkingDirectory)'
        runInParallel: false
        codeCoverageEnabled: true
        testRunTitle: 'UI Tests'
```

### 2. Headless Testing Configuration
```csharp
public static class TestConfiguration
{
    public static IWebDriver CreateDriver()
    {
        var isCI = Environment.GetEnvironmentVariable("CI") == "true";
        
        if (isCI)
        {
            return CreateHeadlessDriver();
        }
        
        return CreateRegularDriver();
    }
    
    private static IWebDriver CreateHeadlessDriver()
    {
        var options = new ChromeOptions();
        options.AddArgument("--headless");
        options.AddArgument("--no-sandbox");
        options.AddArgument("--disable-dev-shm-usage");
        options.AddArgument("--disable-gpu");
        options.AddArgument("--window-size=1920,1080");
        
        return new ChromeDriver(ChromeDriverService.CreateDefaultService(), options, TimeSpan.FromMinutes(3));
    }
    
    private static IWebDriver CreateRegularDriver()
    {
        var options = new ChromeOptions();
        options.AddArgument("--start-maximized");
        
        return new ChromeDriver(options);
    }
}
```

## Best Practices Summary

### 1. Test Design Principles
- **Page Object Model**: Encapsulate page interactions in reusable objects
- **Explicit Waits**: Use WebDriverWait instead of Thread.Sleep
- **Stable Selectors**: Use CSS selectors that handle WebForms dynamic IDs
- **Independent Tests**: Each test should be able to run in isolation
- **Data-Driven Tests**: Use parameterized tests for multiple scenarios

### 2. Element Location Strategies
- **Partial ID Matching**: Use `[id$='controlId']` for WebForms controls
- **Hierarchical Selectors**: Navigate control hierarchies with specific CSS paths
- **Text-Based Selection**: Use link text or partial text when IDs are unstable
- **Custom Attributes**: Add test-specific attributes for reliable element location

### 3. Timing and Synchronization
- **Postback Handling**: Wait for complete page lifecycle after postbacks
- **AJAX Awareness**: Handle UpdatePanel and async postbacks properly
- **Loading States**: Wait for specific elements or conditions, not arbitrary timeouts
- **JavaScript Execution**: Ensure DOM is ready before element interaction

### 4. Test Maintenance
- **Modular Design**: Keep tests focused on single functionality
- **Reusable Components**: Create helper methods for common operations
- **Configuration Management**: Externalize test settings and environment URLs
- **Error Handling**: Implement proper exception handling and reporting

### 5. Performance Considerations
- **Parallel Execution**: Run independent tests in parallel where possible
- **Resource Management**: Properly dispose of WebDriver instances
- **Test Data**: Use efficient test data setup and cleanup strategies
- **Browser Optimization**: Configure browsers for test execution efficiency

This comprehensive UI testing strategy ensures WebForms applications maintain high quality user experiences while providing reliable automated validation of user interface functionality.