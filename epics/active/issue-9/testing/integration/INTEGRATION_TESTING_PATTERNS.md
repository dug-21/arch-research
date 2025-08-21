# WebForms Integration Testing Patterns

## Overview
This guide provides comprehensive strategies for integration testing in ASP.NET WebForms applications, focusing on testing the interactions between different components, systems, and external dependencies.

## Integration Testing Scope

### 1. Component Integration Testing
Testing interactions between WebForms components like user controls, master pages, and pages.

### 2. Database Integration Testing
Testing WebForms application interactions with databases, including data access layers and stored procedures.

### 3. External Service Integration Testing
Testing WebForms integration with web services, APIs, and third-party systems.

### 4. End-to-End Workflow Testing
Testing complete user workflows across multiple pages and systems.

## Database Integration Testing

### 1. Database Setup and Teardown
```csharp
[TestClass]
public class DatabaseIntegrationTestBase
{
    protected string TestConnectionString { get; private set; }
    protected IDbConnection Connection { get; private set; }
    protected IDbTransaction Transaction { get; private set; }
    
    [TestInitialize]
    public virtual void SetupDatabase()
    {
        TestConnectionString = ConfigurationManager.ConnectionStrings["TestDB"].ConnectionString;
        Connection = new SqlConnection(TestConnectionString);
        Connection.Open();
        
        // Start transaction for isolation
        Transaction = Connection.BeginTransaction();
        
        // Seed test data
        SeedTestData();
    }
    
    [TestCleanup]
    public virtual void CleanupDatabase()
    {
        // Rollback transaction to clean up
        Transaction?.Rollback();
        Transaction?.Dispose();
        Connection?.Close();
        Connection?.Dispose();
    }
    
    protected virtual void SeedTestData()
    {
        var seedData = new[]
        {
            "INSERT INTO Customers (Email, Name, Phone) VALUES ('test1@example.com', 'Test Customer 1', '555-0001')",
            "INSERT INTO Customers (Email, Name, Phone) VALUES ('test2@example.com', 'Test Customer 2', '555-0002')",
            "INSERT INTO Orders (CustomerId, OrderDate, Total) VALUES (1, GETDATE(), 100.00)",
            "INSERT INTO Orders (CustomerId, OrderDate, Total) VALUES (2, GETDATE(), 200.00)"
        };
        
        foreach (var sql in seedData)
        {
            using var command = new SqlCommand(sql, (SqlConnection)Connection, (SqlTransaction)Transaction);
            command.ExecuteNonQuery();
        }
    }
    
    protected void ExecuteScript(string script)
    {
        using var command = new SqlCommand(script, (SqlConnection)Connection, (SqlTransaction)Transaction);
        command.ExecuteNonQuery();
    }
    
    protected T ExecuteScalar<T>(string sql)
    {
        using var command = new SqlCommand(sql, (SqlConnection)Connection, (SqlTransaction)Transaction);
        var result = command.ExecuteScalar();
        return result == DBNull.Value ? default(T) : (T)result;
    }
}
```

### 2. Repository Integration Tests
```csharp
[TestClass]
public class CustomerRepositoryIntegrationTests : DatabaseIntegrationTestBase
{
    private CustomerRepository _repository;
    
    [TestInitialize]
    public override void SetupDatabase()
    {
        base.SetupDatabase();
        _repository = new CustomerRepository(TestConnectionString);
        
        // Inject transaction for testing
        _repository.SetTransaction(Transaction);
    }
    
    [TestMethod]
    public void SaveCustomer_ValidCustomer_InsertsToDatabase()
    {
        // Arrange
        var customer = new Customer
        {
            Email = "integration@example.com",
            Name = "Integration Test Customer",
            Phone = "555-9999"
        };
        
        // Act
        var customerId = _repository.Save(customer);
        
        // Assert
        Assert.IsTrue(customerId > 0, "Customer ID should be generated");
        
        // Verify in database
        var savedCustomer = _repository.GetById(customerId);
        Assert.IsNotNull(savedCustomer, "Customer should be retrievable from database");
        Assert.AreEqual(customer.Email, savedCustomer.Email);
        Assert.AreEqual(customer.Name, savedCustomer.Name);
        Assert.AreEqual(customer.Phone, savedCustomer.Phone);
        
        // Verify direct database query
        var dbCustomer = ExecuteScalar<string>(
            $"SELECT Email FROM Customers WHERE Id = {customerId}");
        Assert.AreEqual(customer.Email, dbCustomer);
    }
    
    [TestMethod]
    public void GetCustomersByEmail_PartialMatch_ReturnsMatchingCustomers()
    {
        // Arrange
        var searchTerm = "test";
        
        // Act
        var customers = _repository.GetCustomersByEmail(searchTerm);
        
        // Assert
        Assert.IsTrue(customers.Count >= 2, "Should find at least 2 test customers");
        Assert.IsTrue(customers.All(c => c.Email.Contains(searchTerm)), 
            "All returned customers should match search term");
        
        // Verify against direct database query
        var dbCount = ExecuteScalar<int>(
            "SELECT COUNT(*) FROM Customers WHERE Email LIKE '%test%'");
        Assert.AreEqual(dbCount, customers.Count, 
            "Repository result should match database query");
    }
    
    [TestMethod]
    public void UpdateCustomer_ExistingCustomer_UpdatesDatabase()
    {
        // Arrange
        var originalCustomer = _repository.GetById(1);
        originalCustomer.Name = "Updated Name";
        originalCustomer.Phone = "555-UPDATED";
        
        // Act
        var success = _repository.Update(originalCustomer);
        
        // Assert
        Assert.IsTrue(success, "Update should succeed");
        
        // Verify changes in database
        var updatedCustomer = _repository.GetById(1);
        Assert.AreEqual("Updated Name", updatedCustomer.Name);
        Assert.AreEqual("555-UPDATED", updatedCustomer.Phone);
        
        // Verify with direct database query
        var dbName = ExecuteScalar<string>("SELECT Name FROM Customers WHERE Id = 1");
        Assert.AreEqual("Updated Name", dbName);
    }
    
    [TestMethod]
    public void DeleteCustomer_WithOrders_CascadesCorrectly()
    {
        // Arrange
        var customerId = 1;
        var initialOrderCount = ExecuteScalar<int>(
            $"SELECT COUNT(*) FROM Orders WHERE CustomerId = {customerId}");
        Assert.IsTrue(initialOrderCount > 0, "Customer should have orders for this test");
        
        // Act
        var success = _repository.Delete(customerId);
        
        // Assert
        Assert.IsTrue(success, "Delete should succeed");
        
        // Verify customer is deleted
        var deletedCustomer = _repository.GetById(customerId);
        Assert.IsNull(deletedCustomer, "Customer should be deleted");
        
        // Verify cascade delete of orders (if configured)
        var remainingOrders = ExecuteScalar<int>(
            $"SELECT COUNT(*) FROM Orders WHERE CustomerId = {customerId}");
        Assert.AreEqual(0, remainingOrders, "Orders should be cascade deleted");
    }
    
    [TestMethod]
    public void CustomerRepository_ConcurrentOperations_MaintainsDataIntegrity()
    {
        var tasks = new List<Task<int>>();
        var customerEmails = new List<string>();
        
        // Create multiple concurrent save operations
        for (int i = 0; i < 10; i++)
        {
            var email = $"concurrent{i}@example.com";
            customerEmails.Add(email);
            
            tasks.Add(Task.Run(() =>
            {
                var repo = new CustomerRepository(TestConnectionString);
                repo.SetTransaction(Transaction);
                
                var customer = new Customer
                {
                    Email = email,
                    Name = $"Concurrent Customer {i}",
                    Phone = $"555-000{i}"
                };
                
                return repo.Save(customer);
            }));
        }
        
        // Wait for all operations to complete
        Task.WaitAll(tasks.ToArray());
        
        // Verify all customers were saved
        var savedIds = tasks.Select(t => t.Result).ToList();
        Assert.AreEqual(10, savedIds.Count, "All customers should be saved");
        Assert.IsTrue(savedIds.All(id => id > 0), "All customers should have valid IDs");
        Assert.AreEqual(10, savedIds.Distinct().Count(), "All customer IDs should be unique");
        
        // Verify in database
        foreach (var email in customerEmails)
        {
            var exists = ExecuteScalar<int>(
                $"SELECT COUNT(*) FROM Customers WHERE Email = '{email}'");
            Assert.AreEqual(1, exists, $"Customer with email {email} should exist");
        }
    }
}
```

### 3. Stored Procedure Integration Tests
```csharp
[TestClass]
public class StoredProcedureIntegrationTests : DatabaseIntegrationTestBase
{
    [TestMethod]
    public void GetCustomerOrders_StoredProcedure_ReturnsCorrectData()
    {
        // Arrange
        var customerId = 1;
        
        // Act
        var orders = new List<Order>();
        using var command = new SqlCommand("sp_GetCustomerOrders", (SqlConnection)Connection, (SqlTransaction)Transaction);
        command.CommandType = CommandType.StoredProcedure;
        command.Parameters.AddWithValue("@CustomerId", customerId);
        
        using var reader = command.ExecuteReader();
        while (reader.Read())
        {
            orders.Add(new Order
            {
                Id = reader.GetInt32("Id"),
                CustomerId = reader.GetInt32("CustomerId"),
                OrderDate = reader.GetDateTime("OrderDate"),
                Total = reader.GetDecimal("Total")
            });
        }
        
        // Assert
        Assert.IsTrue(orders.Count > 0, "Should return orders for customer");
        Assert.IsTrue(orders.All(o => o.CustomerId == customerId), 
            "All orders should belong to specified customer");
        
        // Verify against direct query
        var directQueryCount = ExecuteScalar<int>(
            $"SELECT COUNT(*) FROM Orders WHERE CustomerId = {customerId}");
        Assert.AreEqual(directQueryCount, orders.Count, 
            "Stored procedure should return same count as direct query");
    }
    
    [TestMethod]
    public void CreateOrderWithItems_StoredProcedure_HandlesTransaction()
    {
        // Arrange
        var customerId = 1;
        var orderItems = new[]
        {
            new { ProductId = 1, Quantity = 2, Price = 10.00m },
            new { ProductId = 2, Quantity = 1, Price = 25.00m }
        };
        
        // Act
        int orderId;
        using (var command = new SqlCommand("sp_CreateOrderWithItems", (SqlConnection)Connection, (SqlTransaction)Transaction))
        {
            command.CommandType = CommandType.StoredProcedure;
            command.Parameters.AddWithValue("@CustomerId", customerId);
            
            // Create DataTable for order items
            var itemsTable = new DataTable();
            itemsTable.Columns.Add("ProductId", typeof(int));
            itemsTable.Columns.Add("Quantity", typeof(int));
            itemsTable.Columns.Add("Price", typeof(decimal));
            
            foreach (var item in orderItems)
            {
                itemsTable.Rows.Add(item.ProductId, item.Quantity, item.Price);
            }
            
            command.Parameters.AddWithValue("@OrderItems", itemsTable);
            command.Parameters.Add("@OrderId", SqlDbType.Int).Direction = ParameterDirection.Output;
            
            command.ExecuteNonQuery();
            orderId = (int)command.Parameters["@OrderId"].Value;
        }
        
        // Assert
        Assert.IsTrue(orderId > 0, "Order ID should be generated");
        
        // Verify order was created
        var orderExists = ExecuteScalar<int>(
            $"SELECT COUNT(*) FROM Orders WHERE Id = {orderId}");
        Assert.AreEqual(1, orderExists, "Order should be created");
        
        // Verify order items were created
        var itemCount = ExecuteScalar<int>(
            $"SELECT COUNT(*) FROM OrderItems WHERE OrderId = {orderId}");
        Assert.AreEqual(orderItems.Length, itemCount, "All order items should be created");
        
        // Verify total calculation
        var expectedTotal = orderItems.Sum(i => i.Quantity * i.Price);
        var actualTotal = ExecuteScalar<decimal>(
            $"SELECT Total FROM Orders WHERE Id = {orderId}");
        Assert.AreEqual(expectedTotal, actualTotal, "Order total should be calculated correctly");
    }
}
```

## Web Service Integration Testing

### 1. External API Integration Tests
```csharp
[TestClass]
public class ExternalApiIntegrationTests
{
    private HttpClient _httpClient;
    private Mock<IEmailService> _mockEmailService;
    private CustomerService _customerService;
    
    [TestInitialize]
    public void Setup()
    {
        _httpClient = new HttpClient();
        _mockEmailService = new Mock<IEmailService>();
        
        // Setup test configuration
        var config = new Configuration
        {
            ExternalApiBaseUrl = "https://api.example.com",
            ApiKey = "test-api-key"
        };
        
        _customerService = new CustomerService(config, _mockEmailService.Object);
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _httpClient?.Dispose();
    }
    
    [TestMethod]
    public async Task ValidateCustomerAddress_ExternalAPI_ReturnsValidationResult()
    {
        // Arrange
        var customer = new Customer
        {
            Email = "integration@example.com",
            Name = "Integration Test",
            Address = new Address
            {
                Street = "123 Main St",
                City = "Anytown",
                State = "CA",
                ZipCode = "12345"
            }
        };
        
        // Mock external API response
        var mockHandler = new Mock<HttpMessageHandler>();
        mockHandler.Protected()
            .Setup<Task<HttpResponseMessage>>("SendAsync",
                ItExpr.IsAny<HttpRequestMessage>(),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = new StringContent(JsonConvert.SerializeObject(new
                {
                    isValid = true,
                    standardizedAddress = new
                    {
                        street = "123 Main Street",
                        city = "Anytown",
                        state = "CA",
                        zipCode = "12345-0000"
                    }
                }))
            });
        
        var httpClient = new HttpClient(mockHandler.Object);
        var addressValidator = new AddressValidationService(httpClient);
        
        // Act
        var result = await addressValidator.ValidateAsync(customer.Address);
        
        // Assert
        Assert.IsTrue(result.IsValid, "Address should be valid");
        Assert.IsNotNull(result.StandardizedAddress, "Should return standardized address");
        Assert.AreEqual("123 Main Street", result.StandardizedAddress.Street);
        Assert.AreEqual("12345-0000", result.StandardizedAddress.ZipCode);
        
        // Verify API was called correctly
        mockHandler.Protected().Verify("SendAsync",
            Times.Once(),
            ItExpr.Is<HttpRequestMessage>(req =>
                req.Method == HttpMethod.Post &&
                req.RequestUri.ToString().Contains("validate-address")),
            ItExpr.IsAny<CancellationToken>());
    }
    
    [TestMethod]
    public async Task SendWelcomeEmail_EmailService_IntegratesCorrectly()
    {
        // Arrange
        var customer = new Customer
        {
            Id = 123,
            Email = "welcome@example.com",
            Name = "Welcome Test User"
        };
        
        // Setup email service mock
        _mockEmailService.Setup(e => e.SendWelcomeEmailAsync(
            It.IsAny<string>(),
            It.IsAny<string>(),
            It.IsAny<Dictionary<string, string>>()))
            .ReturnsAsync(new EmailResult { IsSuccess = true, MessageId = "email-123" });
        
        // Act
        var result = await _customerService.SendWelcomeEmailAsync(customer);
        
        // Assert
        Assert.IsTrue(result.IsSuccess, "Email should be sent successfully");
        
        // Verify email service was called with correct parameters
        _mockEmailService.Verify(e => e.SendWelcomeEmailAsync(
            customer.Email,
            customer.Name,
            It.Is<Dictionary<string, string>>(dict => 
                dict.ContainsKey("CustomerId") && 
                dict["CustomerId"] == customer.Id.ToString())),
            Times.Once);
    }
    
    [TestMethod]
    public async Task PaymentProcessing_ThirdPartyGateway_HandlesAllScenarios()
    {
        var scenarios = new[]
        {
            new { 
                CardNumber = "4111111111111111", 
                ExpectedResult = PaymentResult.Success,
                Description = "Valid Visa card"
            },
            new { 
                CardNumber = "4000000000000002", 
                ExpectedResult = PaymentResult.Declined,
                Description = "Card declined"
            },
            new { 
                CardNumber = "4000000000000119", 
                ExpectedResult = PaymentResult.ProcessingError,
                Description = "Processing error"
            }
        };
        
        var paymentGateway = new PaymentGatewayService(_httpClient);
        
        foreach (var scenario in scenarios)
        {
            // Arrange
            var paymentRequest = new PaymentRequest
            {
                Amount = 100.00m,
                CardNumber = scenario.CardNumber,
                ExpiryMonth = 12,
                ExpiryYear = 2025,
                CVV = "123"
            };
            
            // Act
            var result = await paymentGateway.ProcessPaymentAsync(paymentRequest);
            
            // Assert
            Assert.AreEqual(scenario.ExpectedResult, result.Status, 
                $"Payment result should match expected for scenario: {scenario.Description}");
            
            if (result.Status == PaymentResult.Success)
            {
                Assert.IsNotNull(result.TransactionId, "Successful payment should have transaction ID");
            }
        }
    }
}
```

### 2. SOAP Web Service Integration
```csharp
[TestClass]
public class SoapWebServiceIntegrationTests
{
    private CustomerWebService _webService;
    
    [TestInitialize]
    public void Setup()
    {
        _webService = new CustomerWebService();
        _webService.Url = "http://localhost:8080/CustomerWebService.asmx";
        
        // Set timeout for integration tests
        _webService.Timeout = 30000; // 30 seconds
    }
    
    [TestMethod]
    public void CreateCustomer_WebService_ReturnsValidResponse()
    {
        // Arrange
        var customerData = new CustomerWebServiceData
        {
            Email = "webservice@example.com",
            Name = "Web Service Test",
            Phone = "555-WEB-SVC"
        };
        
        // Act
        var response = _webService.CreateCustomer(customerData);
        
        // Assert
        Assert.IsNotNull(response, "Web service should return response");
        Assert.IsTrue(response.Success, $"Web service call should succeed: {response.ErrorMessage}");
        Assert.IsTrue(response.CustomerId > 0, "Should return valid customer ID");
        
        // Verify customer was actually created by retrieving it
        var retrievedCustomer = _webService.GetCustomer(response.CustomerId);
        Assert.IsNotNull(retrievedCustomer, "Should be able to retrieve created customer");
        Assert.AreEqual(customerData.Email, retrievedCustomer.Email);
    }
    
    [TestMethod]
    public void GetCustomerList_WebService_ReturnsFilteredResults()
    {
        // Arrange
        var filter = new CustomerFilter
        {
            EmailContains = "example.com",
            CreatedAfter = DateTime.Now.AddDays(-30)
        };
        
        // Act
        var customers = _webService.GetCustomerList(filter);
        
        // Assert
        Assert.IsNotNull(customers, "Web service should return customer list");
        Assert.IsTrue(customers.Length >= 0, "Should return array of customers");
        
        // Verify filtering works
        foreach (var customer in customers)
        {
            Assert.IsTrue(customer.Email.Contains("example.com"), 
                "All customers should match email filter");
            Assert.IsTrue(customer.CreatedDate >= filter.CreatedAfter, 
                "All customers should match date filter");
        }
    }
    
    [TestMethod]
    public void WebService_ErrorHandling_ReturnsAppropriateErrors()
    {
        // Test invalid customer data
        var invalidCustomer = new CustomerWebServiceData
        {
            Email = "invalid-email", // Invalid email format
            Name = "", // Empty name
            Phone = "123" // Invalid phone
        };
        
        var response = _webService.CreateCustomer(invalidCustomer);
        
        Assert.IsNotNull(response, "Should return response even for invalid data");
        Assert.IsFalse(response.Success, "Should indicate failure for invalid data");
        Assert.IsNotNull(response.ErrorMessage, "Should provide error message");
        Assert.IsTrue(response.ErrorMessage.Contains("email") || 
                     response.ErrorMessage.Contains("name") || 
                     response.ErrorMessage.Contains("phone"), 
            "Error message should indicate validation issues");
    }
    
    [TestMethod]
    public void WebService_ConcurrentCalls_HandledCorrectly()
    {
        var tasks = new List<Task<CreateCustomerResponse>>();
        
        // Create multiple concurrent web service calls
        for (int i = 0; i < 5; i++)
        {
            var customerData = new CustomerWebServiceData
            {
                Email = $"concurrent{i}@example.com",
                Name = $"Concurrent Customer {i}",
                Phone = $"555-000{i}"
            };
            
            tasks.Add(Task.Run(() => _webService.CreateCustomer(customerData)));
        }
        
        // Wait for all calls to complete
        Task.WaitAll(tasks.ToArray());
        
        // Verify all calls succeeded
        var responses = tasks.Select(t => t.Result).ToList();
        Assert.IsTrue(responses.All(r => r.Success), "All concurrent calls should succeed");
        
        var customerIds = responses.Select(r => r.CustomerId).ToList();
        Assert.AreEqual(5, customerIds.Distinct().Count(), "All customers should have unique IDs");
    }
}
```

## Page Integration Testing

### 1. Master Page Integration Tests
```csharp
[TestClass]
public class MasterPageIntegrationTests
{
    private TestContext _testContext;
    
    [TestMethod]
    public void CustomerForm_MasterPage_RendersCorrectly()
    {
        // Arrange
        var masterPage = new SiteMaster();
        var contentPage = new CustomerForm();
        
        // Simulate page lifecycle
        var pageContext = CreateTestPageContext();
        
        // Act
        contentPage.Page_Load(null, EventArgs.Empty);
        
        // Assert
        Assert.IsNotNull(contentPage.Master, "Content page should have master page");
        Assert.IsInstanceOfType(contentPage.Master, typeof(SiteMaster));
        
        // Verify master page content
        var siteMaster = (SiteMaster)contentPage.Master;
        Assert.IsNotNull(siteMaster.NavigationMenu, "Master page should have navigation");
        Assert.IsNotNull(siteMaster.HeaderContent, "Master page should have header");
        
        // Verify content page integration
        var titleControl = contentPage.FindControl("PageTitle");
        Assert.IsNotNull(titleControl, "Content page should set page title");
    }
    
    [TestMethod]
    public void Navigation_MasterPage_UpdatesCorrectly()
    {
        // Test navigation highlighting based on current page
        var pages = new[]
        {
            new { Page = "CustomerForm.aspx", ExpectedActiveMenu = "Customers" },
            new { Page = "Reports.aspx", ExpectedActiveMenu = "Reports" },
            new { Page = "Admin.aspx", ExpectedActiveMenu = "Administration" }
        };
        
        foreach (var pageTest in pages)
        {
            var masterPage = new SiteMaster();
            var context = CreateTestPageContext(pageTest.Page);
            
            masterPage.Page_Load(null, EventArgs.Empty);
            
            var activeMenuItem = masterPage.GetActiveMenuItem();
            Assert.AreEqual(pageTest.ExpectedActiveMenu, activeMenuItem, 
                $"Active menu item should be {pageTest.ExpectedActiveMenu} for page {pageTest.Page}");
        }
    }
    
    private HttpContext CreateTestPageContext(string pageName = "CustomerForm.aspx")
    {
        var request = new HttpRequest(pageName, $"http://localhost/{pageName}", "");
        var response = new HttpResponse(new StringWriter());
        var httpContext = new HttpContext(request, response);
        
        HttpContext.Current = httpContext;
        return httpContext;
    }
}
```

### 2. User Control Integration Tests
```csharp
[TestClass]
public class UserControlIntegrationTests
{
    [TestMethod]
    public void CustomerSearchControl_ParentPage_CommunicatesCorrectly()
    {
        // Arrange
        var parentPage = new CustomerManagement();
        var searchControl = new CustomerSearchControl();
        
        // Wire up event handlers
        searchControl.CustomerSelected += parentPage.OnCustomerSelected;
        
        // Simulate user control being added to page
        parentPage.Controls.Add(searchControl);
        
        // Act
        var testCustomer = new Customer { Id = 123, Name = "Test Customer" };
        searchControl.SelectCustomer(testCustomer);
        
        // Assert
        Assert.AreEqual(testCustomer.Id, parentPage.SelectedCustomerId, 
            "Parent page should receive selected customer ID");
        Assert.IsTrue(parentPage.CustomerDetailsVisible, 
            "Parent page should show customer details");
    }
    
    [TestMethod]
    public void AddressControl_Validation_IntegratesWithPage()
    {
        // Arrange
        var page = new CustomerForm();
        var addressControl = new AddressControl();
        page.Controls.Add(addressControl);
        
        // Set invalid address data
        addressControl.Street = "";
        addressControl.City = "";
        addressControl.ZipCode = "invalid";
        
        // Act
        var isValid = page.Validate();
        
        // Assert
        Assert.IsFalse(isValid, "Page validation should fail with invalid address");
        
        var validationErrors = page.GetValidationErrors();
        Assert.IsTrue(validationErrors.Any(e => e.Contains("Street")), 
            "Should have street validation error");
        Assert.IsTrue(validationErrors.Any(e => e.Contains("City")), 
            "Should have city validation error");
        Assert.IsTrue(validationErrors.Any(e => e.Contains("Zip")), 
            "Should have zip code validation error");
    }
    
    [TestMethod]
    public void DataGridControl_Paging_WorksWithDataSource()
    {
        // Arrange
        var gridControl = new CustomerGridControl();
        var customers = GenerateTestCustomers(50); // 50 customers for paging test
        
        gridControl.PageSize = 10;
        gridControl.DataSource = customers;
        
        // Act
        gridControl.DataBind();
        
        // Assert
        Assert.AreEqual(10, gridControl.Items.Count, "Should display page size number of items");
        Assert.AreEqual(5, gridControl.PageCount, "Should calculate correct number of pages");
        Assert.AreEqual(1, gridControl.CurrentPageIndex, "Should start on first page");
        
        // Test paging
        gridControl.CurrentPageIndex = 2;
        gridControl.DataBind();
        
        var firstItemOnPage2 = gridControl.Items[0].DataItem as Customer;
        var expectedFirstItem = customers[10]; // Second page starts at index 10
        
        Assert.AreEqual(expectedFirstItem.Id, firstItemOnPage2.Id, 
            "Second page should show correct items");
    }
    
    private List<Customer> GenerateTestCustomers(int count)
    {
        return Enumerable.Range(1, count)
            .Select(i => new Customer
            {
                Id = i,
                Email = $"customer{i}@example.com",
                Name = $"Customer {i}"
            })
            .ToList();
    }
}
```

## End-to-End Workflow Integration Testing

### 1. Complete User Journey Tests
```csharp
[TestClass]
public class EndToEndWorkflowTests
{
    private IWebDriver _driver;
    private string _baseUrl = "http://localhost:8080";
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
        _driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CompleteCustomerWorkflow_CreateToOrder_WorksEndToEnd()
    {
        var testCustomer = new
        {
            Email = $"workflow{DateTime.Now.Ticks}@example.com",
            Name = "Workflow Test Customer",
            Phone = "555-WORKFLOW"
        };
        
        // Step 1: Create new customer
        _driver.Navigate().GoToUrl($"{_baseUrl}/CustomerForm.aspx");
        
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys(testCustomer.Email);
        _driver.FindElement(By.CssSelector("input[id$='txtName']")).SendKeys(testCustomer.Name);
        _driver.FindElement(By.CssSelector("input[id$='txtPhone']")).SendKeys(testCustomer.Phone);
        _driver.FindElement(By.CssSelector("input[id$='btnSave']")).Click();
        
        // Verify customer creation
        var successMessage = _driver.FindElement(By.CssSelector("span[id$='lblMessage']")).Text;
        Assert.IsTrue(successMessage.Contains("saved"), "Customer should be created successfully");
        
        // Step 2: Search for created customer
        _driver.Navigate().GoToUrl($"{_baseUrl}/CustomerSearch.aspx");
        
        _driver.FindElement(By.CssSelector("input[id$='txtSearchEmail']")).SendKeys(testCustomer.Email);
        _driver.FindElement(By.CssSelector("input[id$='btnSearch']")).Click();
        
        // Verify customer appears in search results
        var searchResults = _driver.FindElements(By.CssSelector("table[id$='GridView1'] tr"));
        Assert.IsTrue(searchResults.Count > 1, "Should find the created customer");
        
        var customerRow = searchResults.FirstOrDefault(row => row.Text.Contains(testCustomer.Email));
        Assert.IsNotNull(customerRow, "Customer should appear in search results");
        
        // Step 3: View customer details
        var viewButton = customerRow.FindElement(By.CssSelector("input[value='View']"));
        viewButton.Click();
        
        // Verify customer details page
        Assert.IsTrue(_driver.Url.Contains("CustomerDetails.aspx"), "Should navigate to customer details");
        Assert.IsTrue(_driver.PageSource.Contains(testCustomer.Name), "Should show customer name");
        Assert.IsTrue(_driver.PageSource.Contains(testCustomer.Email), "Should show customer email");
        
        // Step 4: Create order for customer
        _driver.FindElement(By.CssSelector("input[id$='btnCreateOrder']")).Click();
        
        // Add order items
        _driver.FindElement(By.CssSelector("select[id$='ddlProduct']")).SendKeys("Product 1");
        _driver.FindElement(By.CssSelector("input[id$='txtQuantity']")).SendKeys("2");
        _driver.FindElement(By.CssSelector("input[id$='btnAddItem']")).Click();
        
        _driver.FindElement(By.CssSelector("select[id$='ddlProduct']")).SendKeys("Product 2");
        _driver.FindElement(By.CssSelector("input[id$='txtQuantity']")).SendKeys("1");
        _driver.FindElement(By.CssSelector("input[id$='btnAddItem']")).Click();
        
        // Submit order
        _driver.FindElement(By.CssSelector("input[id$='btnSubmitOrder']")).Click();
        
        // Verify order creation
        var orderMessage = _driver.FindElement(By.CssSelector("span[id$='lblOrderMessage']")).Text;
        Assert.IsTrue(orderMessage.Contains("created"), "Order should be created successfully");
        
        // Step 5: Verify order in order history
        _driver.Navigate().GoToUrl($"{_baseUrl}/OrderHistory.aspx");
        
        _driver.FindElement(By.CssSelector("input[id$='txtCustomerEmail']")).SendKeys(testCustomer.Email);
        _driver.FindElement(By.CssSelector("input[id$='btnSearchOrders']")).Click();
        
        var orderRows = _driver.FindElements(By.CssSelector("table[id$='OrderGridView'] tr"));
        Assert.IsTrue(orderRows.Count > 1, "Should find orders for the customer");
        
        var recentOrder = orderRows[1]; // First data row (skip header)
        Assert.IsTrue(recentOrder.Text.Contains("Product 1"), "Order should contain Product 1");
        Assert.IsTrue(recentOrder.Text.Contains("Product 2"), "Order should contain Product 2");
    }
    
    [TestMethod]
    public void CustomerRegistration_EmailVerification_CompleteFlow()
    {
        var testEmail = $"registration{DateTime.Now.Ticks}@example.com";
        
        // Step 1: Register new customer
        _driver.Navigate().GoToUrl($"{_baseUrl}/Register.aspx");
        
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys(testEmail);
        _driver.FindElement(By.CssSelector("input[id$='txtPassword']")).SendKeys("SecurePassword123!");
        _driver.FindElement(By.CssSelector("input[id$='txtConfirmPassword']")).SendKeys("SecurePassword123!");
        _driver.FindElement(By.CssSelector("input[id$='txtFirstName']")).SendKeys("Test");
        _driver.FindElement(By.CssSelector("input[id$='txtLastName']")).SendKeys("User");
        _driver.FindElement(By.CssSelector("input[id$='btnRegister']")).Click();
        
        // Verify registration success and email verification request
        var registrationMessage = _driver.FindElement(By.CssSelector("span[id$='lblMessage']")).Text;
        Assert.IsTrue(registrationMessage.Contains("verification"), 
            "Should request email verification");
        
        // Step 2: Simulate email verification (get verification token from database)
        var verificationToken = GetVerificationTokenFromDatabase(testEmail);
        Assert.IsNotNull(verificationToken, "Verification token should be generated");
        
        // Step 3: Click verification link
        _driver.Navigate().GoToUrl($"{_baseUrl}/VerifyEmail.aspx?token={verificationToken}");
        
        var verificationMessage = _driver.FindElement(By.CssSelector("span[id$='lblVerificationMessage']")).Text;
        Assert.IsTrue(verificationMessage.Contains("verified"), 
            "Email should be verified successfully");
        
        // Step 4: Login with verified account
        _driver.Navigate().GoToUrl($"{_baseUrl}/Login.aspx");
        
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys(testEmail);
        _driver.FindElement(By.CssSelector("input[id$='txtPassword']")).SendKeys("SecurePassword123!");
        _driver.FindElement(By.CssSelector("input[id$='btnLogin']")).Click();
        
        // Verify successful login
        Assert.IsTrue(_driver.Url.Contains("Dashboard.aspx") || _driver.Url.Contains("Default.aspx"), 
            "Should redirect to dashboard after login");
        
        var welcomeMessage = _driver.FindElement(By.CssSelector("span[id$='lblWelcome']")).Text;
        Assert.IsTrue(welcomeMessage.Contains("Test User"), "Should show user's name");
    }
    
    private string GetVerificationTokenFromDatabase(string email)
    {
        var connectionString = ConfigurationManager.ConnectionStrings["TestDB"].ConnectionString;
        using var connection = new SqlConnection(connectionString);
        connection.Open();
        
        var command = new SqlCommand(
            "SELECT VerificationToken FROM Users WHERE Email = @Email", connection);
        command.Parameters.AddWithValue("@Email", email);
        
        return command.ExecuteScalar()?.ToString();
    }
}
```

## Performance Integration Testing

### 1. Load Testing Integration Points
```csharp
[TestClass]
public class PerformanceIntegrationTests
{
    [TestMethod]
    public void DatabaseConnection_UnderLoad_MaintainsPerformance()
    {
        var connectionString = ConfigurationManager.ConnectionStrings["TestDB"].ConnectionString;
        var tasks = new List<Task<long>>();
        var concurrentUsers = 20;
        var operationsPerUser = 100;
        
        // Simulate concurrent database operations
        for (int user = 0; user < concurrentUsers; user++)
        {
            tasks.Add(Task.Run(() =>
            {
                var stopwatch = Stopwatch.StartNew();
                var repository = new CustomerRepository(connectionString);
                
                for (int op = 0; op < operationsPerUser; op++)
                {
                    var customers = repository.GetAll();
                    var count = customers.Count;
                    
                    // Verify we get data
                    Assert.IsTrue(count >= 0, "Should retrieve customer data");
                }
                
                stopwatch.Stop();
                return stopwatch.ElapsedMilliseconds;
            }));
        }
        
        Task.WaitAll(tasks.ToArray());
        
        // Analyze performance results
        var times = tasks.Select(t => t.Result).ToList();
        var averageTime = times.Average();
        var maxTime = times.Max();
        var minTime = times.Min();
        
        TestContext.WriteLine($"Performance Results:");
        TestContext.WriteLine($"Average time: {averageTime:F2}ms");
        TestContext.WriteLine($"Max time: {maxTime}ms");
        TestContext.WriteLine($"Min time: {minTime}ms");
        
        // Assert performance targets
        Assert.IsTrue(averageTime < 5000, // 5 seconds average
            $"Average response time ({averageTime:F2}ms) exceeds target");
        Assert.IsTrue(maxTime < 10000, // 10 seconds max
            $"Maximum response time ({maxTime}ms) exceeds target");
    }
    
    [TestMethod]
    public void WebServiceIntegration_UnderLoad_RemainsStable()
    {
        var webService = new CustomerWebService();
        webService.Url = "http://localhost:8080/CustomerWebService.asmx";
        
        var tasks = new List<Task<bool>>();
        var concurrentCalls = 10;
        
        for (int i = 0; i < concurrentCalls; i++)
        {
            var callIndex = i;
            tasks.Add(Task.Run(() =>
            {
                try
                {
                    var customer = new CustomerWebServiceData
                    {
                        Email = $"load{callIndex}@example.com",
                        Name = $"Load Test User {callIndex}",
                        Phone = $"555-LOAD{callIndex:D3}"
                    };
                    
                    var response = webService.CreateCustomer(customer);
                    return response.Success;
                }
                catch (Exception ex)
                {
                    TestContext.WriteLine($"Web service call {callIndex} failed: {ex.Message}");
                    return false;
                }
            }));
        }
        
        Task.WaitAll(tasks.ToArray());
        
        var successfulCalls = tasks.Count(t => t.Result);
        var successRate = (double)successfulCalls / concurrentCalls * 100;
        
        TestContext.WriteLine($"Web service success rate: {successRate:F1}%");
        
        Assert.IsTrue(successRate >= 95, 
            $"Web service success rate ({successRate:F1}%) is below target (95%)");
    }
    
    public TestContext TestContext { get; set; }
}
```

## Integration Testing Best Practices

### 1. Test Environment Management
- Use dedicated test databases with known data sets
- Implement proper test data setup and teardown
- Use transactions for test isolation
- Mock external dependencies when appropriate

### 2. Test Data Management
- Create realistic test data scenarios
- Use data builders for complex objects
- Implement test data factories
- Clean up test data after each test

### 3. External Dependency Testing
- Use contract testing for external APIs
- Implement circuit breaker patterns for resilience
- Test timeout and retry scenarios
- Mock external services for reliable testing

### 4. Performance Considerations
- Include performance assertions in integration tests
- Test under realistic load conditions
- Monitor resource usage during tests
- Identify performance bottlenecks early

### 5. Error Handling and Recovery
- Test error scenarios and exception handling
- Verify logging and monitoring integration
- Test recovery mechanisms
- Validate error messages and user experience

This comprehensive integration testing strategy ensures that all components of WebForms applications work together correctly and maintain reliability under various conditions and load scenarios.