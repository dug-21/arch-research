# WebForms Testing Strategies

## Table of Contents
1. [Testing Overview](#testing-overview)
2. [Unit Testing Strategies](#unit-testing-strategies)
3. [Integration Testing Approaches](#integration-testing-approaches)
4. [UI Testing Patterns](#ui-testing-patterns)
5. [Performance Testing](#performance-testing)
6. [Security Testing](#security-testing)
7. [Migration Testing](#migration-testing)
8. [Test Automation Framework](#test-automation-framework)

## Testing Overview

### Testing Challenges in WebForms

WebForms applications present unique testing challenges due to their architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                WebForms Testing Challenges                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Tightly Coupled Architecture                            │
│    • Page lifecycle dependencies                           │
│    • Server control complexity                             │
│    • ViewState management                                  │
│                                                            │
│ 2. Event-Driven Model                                      │
│    • PostBack event handling                              │
│    • Page lifecycle events                                │
│    • Control event cascading                              │
│                                                            │
│ 3. State Management Complexity                            │
│    • ViewState testing                                    │
│    • Session state validation                             │
│    • Control state verification                           │
│                                                            │
│ 4. UI Testing Difficulties                                │
│    • Generated HTML complexity                            │
│    • Control ID changes                                   │
│    • JavaScript integration                               │
└─────────────────────────────────────────────────────────────┘
```

### Testing Strategy Framework

#### Testing Pyramid for WebForms
```
                    /\
                   /UI\  <- Manual/Automated UI Tests
                  /____\
                 /      \
                /   E2E   \  <- End-to-End Integration Tests
               /  Tests    \
              /______________\
             /                \
            /   Integration     \  <- Component Integration Tests
           /      Tests          \
          /________________________\
         /                          \
        /       Unit Tests           \  <- Business Logic Unit Tests
       /                              \
      /________________________________\
```

#### Test Coverage Strategy
| Layer | Coverage Target | Focus Areas | Tools |
|-------|----------------|-------------|-------|
| **Unit Tests** | 80-90% | Business logic, utilities, data access | NUnit, MSTest, xUnit |
| **Integration Tests** | 60-70% | Component interactions, database, APIs | Integration test frameworks |
| **E2E Tests** | 30-40% | Critical user workflows | Selenium, Playwright |
| **UI Tests** | 20-30% | User interface components | UI automation tools |

## Unit Testing Strategies

### Testing Business Logic

#### Separating Business Logic from UI
```csharp
// Bad: Business logic in code-behind
public partial class OrderPage : Page
{
    protected void btnCalculate_Click(object sender, EventArgs e)
    {
        // Business logic embedded in UI event
        decimal subtotal = 0;
        foreach (GridViewRow row in gvItems.Rows)
        {
            var quantity = int.Parse(((TextBox)row.FindControl("txtQuantity")).Text);
            var price = decimal.Parse(((Label)row.FindControl("lblPrice")).Text);
            subtotal += quantity * price;
        }
        
        decimal tax = subtotal * 0.08m;
        decimal shipping = subtotal > 100 ? 0 : 9.99m;
        decimal total = subtotal + tax + shipping;
        
        lblTotal.Text = total.ToString("C");
    }
}

// Good: Business logic in testable service
public class OrderCalculationService
{
    public OrderSummary CalculateOrder(List<OrderItem> items)
    {
        var subtotal = items.Sum(item => item.Quantity * item.Price);
        var tax = subtotal * 0.08m;
        var shipping = subtotal > 100 ? 0 : 9.99m;
        var total = subtotal + tax + shipping;
        
        return new OrderSummary
        {
            Subtotal = subtotal,
            Tax = tax,
            Shipping = shipping,
            Total = total
        };
    }
}

// Unit test for business logic
[TestFixture]
public class OrderCalculationServiceTests
{
    private OrderCalculationService _service;
    
    [SetUp]
    public void Setup()
    {
        _service = new OrderCalculationService();
    }
    
    [Test]
    public void CalculateOrder_WithItemsUnder100_ShouldIncludeShipping()
    {
        // Arrange
        var items = new List<OrderItem>
        {
            new OrderItem { Quantity = 1, Price = 50 },
            new OrderItem { Quantity = 2, Price = 20 }
        };
        
        // Act
        var result = _service.CalculateOrder(items);
        
        // Assert
        Assert.AreEqual(90, result.Subtotal);
        Assert.AreEqual(7.20m, result.Tax);
        Assert.AreEqual(9.99m, result.Shipping);
        Assert.AreEqual(107.19m, result.Total);
    }
    
    [Test]
    public void CalculateOrder_WithItemsOver100_ShouldNotIncludeShipping()
    {
        // Arrange
        var items = new List<OrderItem>
        {
            new OrderItem { Quantity = 1, Price = 150 }
        };
        
        // Act
        var result = _service.CalculateOrder(items);
        
        // Assert
        Assert.AreEqual(150, result.Subtotal);
        Assert.AreEqual(12, result.Tax);
        Assert.AreEqual(0, result.Shipping);
        Assert.AreEqual(162, result.Total);
    }
}
```

### Testing Data Access Layer

#### Repository Pattern Testing
```csharp
// Repository interface
public interface IProductRepository
{
    Product GetById(int id);
    List<Product> GetByCategory(string category);
    void Add(Product product);
    void Update(Product product);
    void Delete(int id);
}

// Repository implementation
public class ProductRepository : IProductRepository
{
    private readonly string _connectionString;
    
    public ProductRepository(string connectionString)
    {
        _connectionString = connectionString;
    }
    
    public Product GetById(int id)
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            using (var command = new SqlCommand("SELECT * FROM Products WHERE Id = @Id", connection))
            {
                command.Parameters.AddWithValue("@Id", id);
                using (var reader = command.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        return new Product
                        {
                            Id = reader.GetInt32("Id"),
                            Name = reader.GetString("Name"),
                            Price = reader.GetDecimal("Price"),
                            Category = reader.GetString("Category")
                        };
                    }
                }
            }
        }
        return null;
    }
    
    // Other methods...
}

// Integration test with test database
[TestFixture]
public class ProductRepositoryTests
{
    private string _connectionString;
    private ProductRepository _repository;
    
    [SetUp]
    public void Setup()
    {
        _connectionString = ConfigurationManager.ConnectionStrings["TestDatabase"].ConnectionString;
        _repository = new ProductRepository(_connectionString);
        SeedTestData();
    }
    
    [TearDown]
    public void TearDown()
    {
        CleanupTestData();
    }
    
    [Test]
    public void GetById_WithValidId_ShouldReturnProduct()
    {
        // Act
        var product = _repository.GetById(1);
        
        // Assert
        Assert.IsNotNull(product);
        Assert.AreEqual(1, product.Id);
        Assert.AreEqual("Test Product", product.Name);
    }
    
    [Test]
    public void GetById_WithInvalidId_ShouldReturnNull()
    {
        // Act
        var product = _repository.GetById(999);
        
        // Assert
        Assert.IsNull(product);
    }
    
    [Test]
    public void Add_WithValidProduct_ShouldInsertProduct()
    {
        // Arrange
        var product = new Product
        {
            Name = "New Product",
            Price = 29.99m,
            Category = "Electronics"
        };
        
        // Act
        _repository.Add(product);
        
        // Assert
        var insertedProduct = _repository.GetByCategory("Electronics")
            .FirstOrDefault(p => p.Name == "New Product");
        Assert.IsNotNull(insertedProduct);
        Assert.AreEqual(29.99m, insertedProduct.Price);
    }
    
    private void SeedTestData()
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            using (var command = new SqlCommand(
                "INSERT INTO Products (Id, Name, Price, Category) VALUES (1, 'Test Product', 19.99, 'Test')", 
                connection))
            {
                command.ExecuteNonQuery();
            }
        }
    }
    
    private void CleanupTestData()
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            using (var command = new SqlCommand("DELETE FROM Products", connection))
            {
                command.ExecuteNonQuery();
            }
        }
    }
}
```

### Testing Page Logic with MVP Pattern

#### Presenter Testing
```csharp
// View interface
public interface IProductView
{
    string ProductName { get; set; }
    decimal Price { get; set; }
    string Category { get; set; }
    List<Product> Products { set; }
    void ShowMessage(string message);
    void ShowError(string error);
    
    event EventHandler SaveClicked;
    event EventHandler LoadClicked;
}

// Presenter
public class ProductPresenter
{
    private readonly IProductView _view;
    private readonly IProductRepository _repository;
    
    public ProductPresenter(IProductView view, IProductRepository repository)
    {
        _view = view;
        _repository = repository;
        
        _view.SaveClicked += OnSaveClicked;
        _view.LoadClicked += OnLoadClicked;
    }
    
    private void OnSaveClicked(object sender, EventArgs e)
    {
        try
        {
            if (string.IsNullOrEmpty(_view.ProductName))
            {
                _view.ShowError("Product name is required");
                return;
            }
            
            var product = new Product
            {
                Name = _view.ProductName,
                Price = _view.Price,
                Category = _view.Category
            };
            
            _repository.Add(product);
            _view.ShowMessage("Product saved successfully");
            LoadProducts();
        }
        catch (Exception ex)
        {
            _view.ShowError($"Error saving product: {ex.Message}");
        }
    }
    
    private void OnLoadClicked(object sender, EventArgs e)
    {
        LoadProducts();
    }
    
    private void LoadProducts()
    {
        try
        {
            var products = _repository.GetByCategory(_view.Category);
            _view.Products = products;
        }
        catch (Exception ex)
        {
            _view.ShowError($"Error loading products: {ex.Message}");
        }
    }
}

// Presenter unit tests
[TestFixture]
public class ProductPresenterTests
{
    private Mock<IProductView> _mockView;
    private Mock<IProductRepository> _mockRepository;
    private ProductPresenter _presenter;
    
    [SetUp]
    public void Setup()
    {
        _mockView = new Mock<IProductView>();
        _mockRepository = new Mock<IProductRepository>();
        _presenter = new ProductPresenter(_mockView.Object, _mockRepository.Object);
    }
    
    [Test]
    public void SaveClicked_WithValidProduct_ShouldSaveProduct()
    {
        // Arrange
        _mockView.SetupGet(v => v.ProductName).Returns("Test Product");
        _mockView.SetupGet(v => v.Price).Returns(19.99m);
        _mockView.SetupGet(v => v.Category).Returns("Electronics");
        
        // Act
        _mockView.Raise(v => v.SaveClicked += null, EventArgs.Empty);
        
        // Assert
        _mockRepository.Verify(r => r.Add(It.Is<Product>(p => 
            p.Name == "Test Product" && 
            p.Price == 19.99m && 
            p.Category == "Electronics")), Times.Once);
        _mockView.Verify(v => v.ShowMessage("Product saved successfully"), Times.Once);
    }
    
    [Test]
    public void SaveClicked_WithEmptyName_ShouldShowError()
    {
        // Arrange
        _mockView.SetupGet(v => v.ProductName).Returns("");
        
        // Act
        _mockView.Raise(v => v.SaveClicked += null, EventArgs.Empty);
        
        // Assert
        _mockRepository.Verify(r => r.Add(It.IsAny<Product>()), Times.Never);
        _mockView.Verify(v => v.ShowError("Product name is required"), Times.Once);
    }
    
    [Test]
    public void SaveClicked_WithRepositoryException_ShouldShowError()
    {
        // Arrange
        _mockView.SetupGet(v => v.ProductName).Returns("Test Product");
        _mockRepository.Setup(r => r.Add(It.IsAny<Product>()))
            .Throws(new Exception("Database error"));
        
        // Act
        _mockView.Raise(v => v.SaveClicked += null, EventArgs.Empty);
        
        // Assert
        _mockView.Verify(v => v.ShowError("Error saving product: Database error"), Times.Once);
    }
}
```

## Integration Testing Approaches

### Testing Page Integration

#### Page Integration Test Framework
```csharp
// Base class for page integration tests
public abstract class PageIntegrationTestBase
{
    protected HttpContext CreateHttpContext(string url = "http://localhost/test.aspx")
    {
        var request = new HttpRequest("test.aspx", url, "");
        var response = new HttpResponse(new StringWriter());
        var context = new HttpContext(request, response);
        
        HttpContext.Current = context;
        return context;
    }
    
    protected T CreatePage<T>() where T : Page, new()
    {
        var page = new T();
        var context = CreateHttpContext();
        
        // Initialize page context
        page.Context = context;
        page.Request = context.Request;
        page.Response = context.Response;
        page.Server = context.Server;
        
        return page;
    }
    
    protected void SimulatePageLifecycle(Page page)
    {
        // Simulate page lifecycle events
        page.ProcessRequest(page.Context);
    }
}

// Page integration test
[TestFixture]
public class ProductPageIntegrationTests : PageIntegrationTestBase
{
    private ProductPage _page;
    private TestDatabase _testDb;
    
    [SetUp]
    public void Setup()
    {
        _testDb = new TestDatabase();
        _testDb.Initialize();
        
        _page = CreatePage<ProductPage>();
    }
    
    [TearDown]
    public void TearDown()
    {
        _testDb.Cleanup();
    }
    
    [Test]
    public void Page_Load_ShouldLoadProducts()
    {
        // Arrange
        _testDb.SeedProducts();
        
        // Act
        SimulatePageLifecycle(_page);
        
        // Assert
        var gridView = _page.FindControl("gvProducts") as GridView;
        Assert.IsNotNull(gridView);
        Assert.Greater(gridView.Rows.Count, 0);
    }
    
    [Test]
    public void AddProduct_WithValidData_ShouldAddProduct()
    {
        // Arrange
        var txtName = _page.FindControl("txtProductName") as TextBox;
        var txtPrice = _page.FindControl("txtPrice") as TextBox;
        var btnAdd = _page.FindControl("btnAdd") as Button;
        
        txtName.Text = "New Product";
        txtPrice.Text = "29.99";
        
        // Act
        SimulateButtonClick(btnAdd);
        
        // Assert
        var products = _testDb.GetProducts();
        Assert.AreEqual(1, products.Count(p => p.Name == "New Product"));
    }
    
    private void SimulateButtonClick(Button button)
    {
        // Simulate button click event
        var eventArgs = new EventArgs();
        button.GetType()
            .GetMethod("OnClick", BindingFlags.NonPublic | BindingFlags.Instance)
            .Invoke(button, new object[] { eventArgs });
    }
}
```

### Testing External Integrations

#### API Integration Testing
```csharp
// External service interface
public interface IPaymentService
{
    PaymentResult ProcessPayment(PaymentRequest request);
}

// Service implementation
public class PaymentService : IPaymentService
{
    private readonly string _apiUrl;
    private readonly string _apiKey;
    
    public PaymentService(string apiUrl, string apiKey)
    {
        _apiUrl = apiUrl;
        _apiKey = apiKey;
    }
    
    public PaymentResult ProcessPayment(PaymentRequest request)
    {
        using (var client = new WebClient())
        {
            client.Headers.Add("Authorization", $"Bearer {_apiKey}");
            client.Headers.Add("Content-Type", "application/json");
            
            var json = JsonConvert.SerializeObject(request);
            var responseJson = client.UploadString(_apiUrl + "/payments", json);
            
            return JsonConvert.DeserializeObject<PaymentResult>(responseJson);
        }
    }
}

// Integration test with mock server
[TestFixture]
public class PaymentServiceIntegrationTests
{
    private MockServer _mockServer;
    private PaymentService _service;
    
    [SetUp]
    public void Setup()
    {
        _mockServer = new MockServer(8080);
        _mockServer.Start();
        
        _service = new PaymentService("http://localhost:8080", "test-api-key");
    }
    
    [TearDown]
    public void TearDown()
    {
        _mockServer.Stop();
    }
    
    [Test]
    public void ProcessPayment_WithValidRequest_ShouldReturnSuccess()
    {
        // Arrange
        _mockServer.SetupResponse("/payments", 
            new PaymentResult { Success = true, TransactionId = "TXN123" });
        
        var request = new PaymentRequest
        {
            Amount = 100.00m,
            CardNumber = "4111111111111111",
            ExpiryMonth = 12,
            ExpiryYear = 2025
        };
        
        // Act
        var result = _service.ProcessPayment(request);
        
        // Assert
        Assert.IsTrue(result.Success);
        Assert.AreEqual("TXN123", result.TransactionId);
    }
    
    [Test]
    public void ProcessPayment_WithInvalidCard_ShouldReturnFailure()
    {
        // Arrange
        _mockServer.SetupResponse("/payments", 
            new PaymentResult { Success = false, ErrorMessage = "Invalid card number" });
        
        var request = new PaymentRequest
        {
            Amount = 100.00m,
            CardNumber = "1234567890123456",
            ExpiryMonth = 12,
            ExpiryYear = 2025
        };
        
        // Act
        var result = _service.ProcessPayment(request);
        
        // Assert
        Assert.IsFalse(result.Success);
        Assert.AreEqual("Invalid card number", result.ErrorMessage);
    }
}
```

## UI Testing Patterns

### Selenium WebDriver Testing

#### Page Object Model for WebForms
```csharp
// Base page object
public abstract class BasePageObject
{
    protected readonly IWebDriver Driver;
    protected readonly WebDriverWait Wait;
    
    protected BasePageObject(IWebDriver driver)
    {
        Driver = driver;
        Wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
    }
    
    protected IWebElement FindElement(By locator)
    {
        return Wait.Until(ExpectedConditions.ElementToBeClickable(locator));
    }
    
    protected IList<IWebElement> FindElements(By locator)
    {
        return Driver.FindElements(locator);
    }
    
    protected void WaitForPageLoad()
    {
        Wait.Until(driver => ((IJavaScriptExecutor)driver)
            .ExecuteScript("return document.readyState").Equals("complete"));
    }
    
    protected string GetControlId(string serverControlId)
    {
        // Handle WebForms control ID mangling
        var element = Driver.FindElement(By.XPath($"//*[contains(@id, '{serverControlId}')]"));
        return element.GetAttribute("id");
    }
}

// Product page object
public class ProductPageObject : BasePageObject
{
    private readonly By _productNameTextBox = By.Id("txtProductName");
    private readonly By _priceTextBox = By.Id("txtPrice");
    private readonly By _categoryDropDown = By.Id("ddlCategory");
    private readonly By _addButton = By.Id("btnAdd");
    private readonly By _productsGrid = By.Id("gvProducts");
    private readonly By _messageLabel = By.Id("lblMessage");
    
    public ProductPageObject(IWebDriver driver) : base(driver)
    {
    }
    
    public void EnterProductName(string name)
    {
        var textBox = FindElement(_productNameTextBox);
        textBox.Clear();
        textBox.SendKeys(name);
    }
    
    public void EnterPrice(decimal price)
    {
        var textBox = FindElement(_priceTextBox);
        textBox.Clear();
        textBox.SendKeys(price.ToString());
    }
    
    public void SelectCategory(string category)
    {
        var dropdown = new SelectElement(FindElement(_categoryDropDown));
        dropdown.SelectByText(category);
    }
    
    public void ClickAddButton()
    {
        FindElement(_addButton).Click();
        WaitForPostBack();
    }
    
    public int GetProductCount()
    {
        var grid = FindElement(_productsGrid);
        var rows = grid.FindElements(By.TagName("tr"));
        return rows.Count - 1; // Subtract header row
    }
    
    public string GetMessage()
    {
        return FindElement(_messageLabel).Text;
    }
    
    private void WaitForPostBack()
    {
        // Wait for WebForms postback to complete
        Wait.Until(driver => 
        {
            var script = "return typeof(Sys) !== 'undefined' && Sys.WebForms && Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() === false;";
            return (bool)((IJavaScriptExecutor)driver).ExecuteScript(script);
        });
    }
}

// UI test class
[TestFixture]
public class ProductPageUITests
{
    private IWebDriver _driver;
    private ProductPageObject _productPage;
    
    [SetUp]
    public void Setup()
    {
        _driver = new ChromeDriver();
        _driver.Navigate().GoToUrl("http://localhost:8080/Products.aspx");
        _productPage = new ProductPageObject(_driver);
    }
    
    [TearDown]
    public void TearDown()
    {
        _driver?.Quit();
    }
    
    [Test]
    public void AddProduct_WithValidData_ShouldDisplayProduct()
    {
        // Arrange
        var initialCount = _productPage.GetProductCount();
        
        // Act
        _productPage.EnterProductName("Test Product");
        _productPage.EnterPrice(29.99m);
        _productPage.SelectCategory("Electronics");
        _productPage.ClickAddButton();
        
        // Assert
        Assert.AreEqual(initialCount + 1, _productPage.GetProductCount());
        Assert.AreEqual("Product added successfully", _productPage.GetMessage());
    }
    
    [Test]
    public void AddProduct_WithEmptyName_ShouldShowError()
    {
        // Act
        _productPage.EnterProductName("");
        _productPage.EnterPrice(29.99m);
        _productPage.ClickAddButton();
        
        // Assert
        Assert.AreEqual("Product name is required", _productPage.GetMessage());
    }
}
```

### Testing AJAX and UpdatePanel

#### UpdatePanel Testing
```csharp
public class UpdatePanelTestHelper
{
    private readonly IWebDriver _driver;
    private readonly WebDriverWait _wait;
    
    public UpdatePanelTestHelper(IWebDriver driver)
    {
        _driver = driver;
        _wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
    }
    
    public void WaitForUpdatePanelUpdate()
    {
        // Wait for UpdatePanel postback to complete
        _wait.Until(driver =>
        {
            var script = @"
                return typeof(Sys) !== 'undefined' && 
                       Sys.WebForms && 
                       Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() === false;";
            return (bool)((IJavaScriptExecutor)driver).ExecuteScript(script);
        });
    }
    
    public void WaitForElementUpdate(By elementLocator)
    {
        var originalElement = _driver.FindElement(elementLocator);
        var originalText = originalElement.Text;
        
        _wait.Until(driver =>
        {
            var currentElement = driver.FindElement(elementLocator);
            return !currentElement.Text.Equals(originalText);
        });
    }
}

[TestFixture]
public class AjaxEnabledPageTests
{
    private IWebDriver _driver;
    private UpdatePanelTestHelper _ajaxHelper;
    
    [SetUp]
    public void Setup()
    {
        _driver = new ChromeDriver();
        _ajaxHelper = new UpdatePanelTestHelper(_driver);
        _driver.Navigate().GoToUrl("http://localhost:8080/AjaxPage.aspx");
    }
    
    [Test]
    public void UpdatePanel_Refresh_ShouldUpdateContent()
    {
        // Arrange
        var refreshButton = _driver.FindElement(By.Id("btnRefresh"));
        var contentLabel = _driver.FindElement(By.Id("lblContent"));
        var originalContent = contentLabel.Text;
        
        // Act
        refreshButton.Click();
        _ajaxHelper.WaitForUpdatePanelUpdate();
        
        // Assert
        var updatedContent = contentLabel.Text;
        Assert.AreNotEqual(originalContent, updatedContent);
    }
}
```

## Performance Testing

### Load Testing WebForms Applications

#### Performance Test Framework
```csharp
public class WebFormsPerformanceTest
{
    private readonly string _baseUrl;
    private readonly int _maxConcurrentUsers;
    
    public WebFormsPerformanceTest(string baseUrl, int maxConcurrentUsers)
    {
        _baseUrl = baseUrl;
        _maxConcurrentUsers = maxConcurrentUsers;
    }
    
    public async Task<PerformanceTestResult> RunLoadTest(string pagePath, int durationMinutes)
    {
        var results = new List<RequestResult>();
        var cancellationToken = new CancellationTokenSource(TimeSpan.FromMinutes(durationMinutes));
        
        var tasks = Enumerable.Range(0, _maxConcurrentUsers)
            .Select(i => SimulateUser(pagePath, cancellationToken.Token, results))
            .ToArray();
        
        await Task.WhenAll(tasks);
        
        return AnalyzeResults(results);
    }
    
    private async Task SimulateUser(string pagePath, CancellationToken cancellationToken, List<RequestResult> results)
    {
        using (var client = new HttpClient())
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                var stopwatch = Stopwatch.StartNew();
                
                try
                {
                    var response = await client.GetAsync($"{_baseUrl}/{pagePath}");
                    stopwatch.Stop();
                    
                    lock (results)
                    {
                        results.Add(new RequestResult
                        {
                            ResponseTime = stopwatch.ElapsedMilliseconds,
                            StatusCode = (int)response.StatusCode,
                            Success = response.IsSuccessStatusCode,
                            Timestamp = DateTime.Now
                        });
                    }
                }
                catch (Exception ex)
                {
                    stopwatch.Stop();
                    
                    lock (results)
                    {
                        results.Add(new RequestResult
                        {
                            ResponseTime = stopwatch.ElapsedMilliseconds,
                            Success = false,
                            Error = ex.Message,
                            Timestamp = DateTime.Now
                        });
                    }
                }
                
                await Task.Delay(1000, cancellationToken); // 1 second between requests
            }
        }
    }
    
    private PerformanceTestResult AnalyzeResults(List<RequestResult> results)
    {
        var successfulRequests = results.Where(r => r.Success).ToList();
        var failedRequests = results.Where(r => !r.Success).ToList();
        
        return new PerformanceTestResult
        {
            TotalRequests = results.Count,
            SuccessfulRequests = successfulRequests.Count,
            FailedRequests = failedRequests.Count,
            AverageResponseTime = successfulRequests.Average(r => r.ResponseTime),
            MinResponseTime = successfulRequests.Min(r => r.ResponseTime),
            MaxResponseTime = successfulRequests.Max(r => r.ResponseTime),
            Percentile95 = CalculatePercentile(successfulRequests.Select(r => r.ResponseTime), 95),
            RequestsPerSecond = results.Count / (results.Max(r => r.Timestamp) - results.Min(r => r.Timestamp)).TotalSeconds
        };
    }
    
    private double CalculatePercentile(IEnumerable<long> values, int percentile)
    {
        var sortedValues = values.OrderBy(v => v).ToArray();
        var index = (int)Math.Ceiling(sortedValues.Length * percentile / 100.0) - 1;
        return sortedValues[index];
    }
}

// Performance test usage
[TestFixture]
public class WebFormsPerformanceTests
{
    [Test]
    public async Task ProductPage_LoadTest_ShouldMeetPerformanceTargets()
    {
        // Arrange
        var performanceTest = new WebFormsPerformanceTest("http://localhost:8080", 10);
        
        // Act
        var result = await performanceTest.RunLoadTest("Products.aspx", 5);
        
        // Assert
        Assert.Less(result.AverageResponseTime, 2000, "Average response time should be less than 2 seconds");
        Assert.Less(result.Percentile95, 5000, "95th percentile should be less than 5 seconds");
        Assert.Greater(result.RequestsPerSecond, 5, "Should handle at least 5 requests per second");
        Assert.Less(result.FailedRequests / (double)result.TotalRequests, 0.01, "Error rate should be less than 1%");
    }
}
```

### ViewState Performance Testing

#### ViewState Size Monitoring
```csharp
public class ViewStateAnalyzer
{
    public ViewStateAnalysisResult AnalyzeViewState(string html)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);
        
        var viewStateInput = doc.DocumentNode
            .SelectSingleNode("//input[@id='__VIEWSTATE']");
            
        if (viewStateInput == null)
        {
            return new ViewStateAnalysisResult { HasViewState = false };
        }
        
        var viewStateValue = viewStateInput.GetAttributeValue("value", "");
        var viewStateBytes = Convert.FromBase64String(viewStateValue);
        
        return new ViewStateAnalysisResult
        {
            HasViewState = true,
            ViewStateSizeBytes = viewStateBytes.Length,
            ViewStateSizeKB = viewStateBytes.Length / 1024.0,
            IsCompressed = IsCompressed(viewStateBytes),
            DecompressedSize = GetDecompressedSize(viewStateBytes)
        };
    }
    
    private bool IsCompressed(byte[] data)
    {
        // Check for GZIP header
        return data.Length > 2 && data[0] == 0x1f && data[1] == 0x8b;
    }
    
    private int GetDecompressedSize(byte[] data)
    {
        if (!IsCompressed(data))
            return data.Length;
            
        try
        {
            using (var stream = new MemoryStream(data))
            using (var gzip = new GZipStream(stream, CompressionMode.Decompress))
            using (var output = new MemoryStream())
            {
                gzip.CopyTo(output);
                return (int)output.Length;
            }
        }
        catch
        {
            return data.Length;
        }
    }
}

[TestFixture]
public class ViewStatePerformanceTests
{
    private ViewStateAnalyzer _analyzer;
    
    [SetUp]
    public void Setup()
    {
        _analyzer = new ViewStateAnalyzer();
    }
    
    [Test]
    public void ProductPage_ViewStateSize_ShouldBeBelowThreshold()
    {
        // Arrange
        using (var client = new WebClient())
        {
            var html = client.DownloadString("http://localhost:8080/Products.aspx");
            
            // Act
            var result = _analyzer.AnalyzeViewState(html);
            
            // Assert
            Assert.IsTrue(result.HasViewState);
            Assert.Less(result.ViewStateSizeKB, 100, "ViewState should be less than 100KB");
            
            if (result.IsCompressed)
            {
                var compressionRatio = result.DecompressedSize / (double)result.ViewStateSizeBytes;
                Assert.Greater(compressionRatio, 2, "ViewState compression ratio should be at least 2:1");
            }
        }
    }
}
```

## Security Testing

### Authentication Testing

#### Authentication Test Framework
```csharp
public class AuthenticationTestHelper
{
    private readonly string _baseUrl;
    
    public AuthenticationTestHelper(string baseUrl)
    {
        _baseUrl = baseUrl;
    }
    
    public async Task<AuthenticationResult> TestLogin(string username, string password)
    {
        var cookieContainer = new CookieContainer();
        
        using (var handler = new HttpClientHandler { CookieContainer = cookieContainer })
        using (var client = new HttpClient(handler))
        {
            // Get login page
            var loginPageResponse = await client.GetAsync($"{_baseUrl}/Login.aspx");
            var loginPageHtml = await loginPageResponse.Content.ReadAsStringAsync();
            
            // Extract ViewState and EventValidation
            var viewState = ExtractHiddenField(loginPageHtml, "__VIEWSTATE");
            var eventValidation = ExtractHiddenField(loginPageHtml, "__EVENTVALIDATION");
            
            // Prepare login data
            var loginData = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("__VIEWSTATE", viewState),
                new KeyValuePair<string, string>("__EVENTVALIDATION", eventValidation),
                new KeyValuePair<string, string>("txtUsername", username),
                new KeyValuePair<string, string>("txtPassword", password),
                new KeyValuePair<string, string>("btnLogin", "Login")
            });
            
            // Submit login
            var loginResponse = await client.PostAsync($"{_baseUrl}/Login.aspx", loginData);
            
            return new AuthenticationResult
            {
                Success = !loginResponse.RequestMessage.RequestUri.AbsolutePath.Contains("Login.aspx"),
                ResponseUrl = loginResponse.RequestMessage.RequestUri.ToString(),
                StatusCode = loginResponse.StatusCode,
                Cookies = cookieContainer.GetCookies(new Uri(_baseUrl)).Cast<Cookie>().ToList()
            };
        }
    }
    
    public async Task<bool> TestAuthorization(string pageUrl, List<Cookie> authCookies)
    {
        var cookieContainer = new CookieContainer();
        
        // Add authentication cookies
        foreach (var cookie in authCookies)
        {
            cookieContainer.Add(cookie);
        }
        
        using (var handler = new HttpClientHandler { CookieContainer = cookieContainer })
        using (var client = new HttpClient(handler))
        {
            var response = await client.GetAsync($"{_baseUrl}/{pageUrl}");
            return response.IsSuccessStatusCode && 
                   !response.RequestMessage.RequestUri.AbsolutePath.Contains("Login.aspx");
        }
    }
    
    private string ExtractHiddenField(string html, string fieldName)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);
        
        var input = doc.DocumentNode
            .SelectSingleNode($"//input[@name='{fieldName}']");
            
        return input?.GetAttributeValue("value", "") ?? "";
    }
}

[TestFixture]
public class SecurityTests
{
    private AuthenticationTestHelper _authHelper;
    
    [SetUp]
    public void Setup()
    {
        _authHelper = new AuthenticationTestHelper("http://localhost:8080");
    }
    
    [Test]
    public async Task Login_WithValidCredentials_ShouldSucceed()
    {
        // Act
        var result = await _authHelper.TestLogin("admin", "password123");
        
        // Assert
        Assert.IsTrue(result.Success);
        Assert.IsFalse(result.ResponseUrl.Contains("Login.aspx"));
        Assert.IsTrue(result.Cookies.Any(c => c.Name.Contains("Auth")));
    }
    
    [Test]
    public async Task Login_WithInvalidCredentials_ShouldFail()
    {
        // Act
        var result = await _authHelper.TestLogin("admin", "wrongpassword");
        
        // Assert
        Assert.IsFalse(result.Success);
        Assert.IsTrue(result.ResponseUrl.Contains("Login.aspx"));
    }
    
    [Test]
    public async Task ProtectedPage_WithoutAuthentication_ShouldRedirectToLogin()
    {
        // Act
        var authorized = await _authHelper.TestAuthorization("Admin/Users.aspx", new List<Cookie>());
        
        // Assert
        Assert.IsFalse(authorized);
    }
    
    [Test]
    public async Task ProtectedPage_WithAuthentication_ShouldAllowAccess()
    {
        // Arrange
        var loginResult = await _authHelper.TestLogin("admin", "password123");
        
        // Act
        var authorized = await _authHelper.TestAuthorization("Admin/Users.aspx", loginResult.Cookies);
        
        // Assert
        Assert.IsTrue(authorized);
    }
}
```

### Input Validation Testing

#### Security Vulnerability Testing
```csharp
[TestFixture]
public class InputValidationTests
{
    private IWebDriver _driver;
    
    [SetUp]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TearDown]
    public void TearDown()
    {
        _driver?.Quit();
    }
    
    [Test]
    public void ContactForm_XSSAttack_ShouldBeBlocked()
    {
        // Arrange
        _driver.Navigate().GoToUrl("http://localhost:8080/Contact.aspx");
        var nameField = _driver.FindElement(By.Id("txtName"));
        var messageField = _driver.FindElement(By.Id("txtMessage"));
        var submitButton = _driver.FindElement(By.Id("btnSubmit"));
        
        var xssPayload = "<script>alert('XSS')</script>";
        
        // Act
        nameField.SendKeys(xssPayload);
        messageField.SendKeys("Test message");
        submitButton.Click();
        
        // Assert
        var pageSource = _driver.PageSource;
        Assert.IsFalse(pageSource.Contains("<script>alert('XSS')</script>"));
        Assert.IsTrue(pageSource.Contains("&lt;script&gt;alert('XSS')&lt;/script&gt;"));
    }
    
    [Test]
    public void SearchForm_SQLInjection_ShouldBeBlocked()
    {
        // Arrange
        _driver.Navigate().GoToUrl("http://localhost:8080/Search.aspx");
        var searchField = _driver.FindElement(By.Id("txtSearch"));
        var searchButton = _driver.FindElement(By.Id("btnSearch"));
        
        var sqlInjectionPayload = "'; DROP TABLE Users; --";
        
        // Act
        searchField.SendKeys(sqlInjectionPayload);
        searchButton.Click();
        
        // Assert
        var errorElement = _driver.FindElements(By.ClassName("error-message"));
        if (errorElement.Any())
        {
            var errorText = errorElement.First().Text;
            Assert.IsFalse(errorText.Contains("syntax error") || errorText.Contains("SQL"));
        }
    }
}
```

## Migration Testing

### Side-by-Side Comparison Testing

#### Migration Validation Framework
```csharp
public class MigrationTestFramework
{
    private readonly string _legacyUrl;
    private readonly string _modernUrl;
    
    public MigrationTestFramework(string legacyUrl, string modernUrl)
    {
        _legacyUrl = legacyUrl;
        _modernUrl = modernUrl;
    }
    
    public async Task<ComparisonResult> ComparePages(string pagePath, Dictionary<string, string> testData)
    {
        var legacyResult = await TestPage(_legacyUrl + "/" + pagePath, testData);
        var modernResult = await TestPage(_modernUrl + "/" + pagePath, testData);
        
        return new ComparisonResult
        {
            LegacyResult = legacyResult,
            ModernResult = modernResult,
            FunctionallyEquivalent = CompareFunctionality(legacyResult, modernResult),
            PerformanceImprovement = CalculatePerformanceImprovement(legacyResult, modernResult)
        };
    }
    
    private async Task<PageTestResult> TestPage(string url, Dictionary<string, string> testData)
    {
        var stopwatch = Stopwatch.StartNew();
        
        using (var driver = new ChromeDriver())
        {
            driver.Navigate().GoToUrl(url);
            
            // Fill in test data
            foreach (var data in testData)
            {
                var element = driver.FindElement(By.Id(data.Key));
                element.Clear();
                element.SendKeys(data.Value);
            }
            
            // Submit form
            var submitButton = driver.FindElement(By.XPath("//input[@type='submit']"));
            submitButton.Click();
            
            stopwatch.Stop();
            
            // Capture results
            var pageSource = driver.PageSource;
            var screenshots = TakeScreenshot(driver);
            
            return new PageTestResult
            {
                ResponseTime = stopwatch.ElapsedMilliseconds,
                PageSource = pageSource,
                Screenshot = screenshots,
                Success = !pageSource.Contains("error") && !pageSource.Contains("exception")
            };
        }
    }
    
    private bool CompareFunctionality(PageTestResult legacy, PageTestResult modern)
    {
        // Extract key functional elements
        var legacyData = ExtractKeyData(legacy.PageSource);
        var modernData = ExtractKeyData(modern.PageSource);
        
        return legacyData.SequenceEqual(modernData);
    }
    
    private double CalculatePerformanceImprovement(PageTestResult legacy, PageTestResult modern)
    {
        return (legacy.ResponseTime - modern.ResponseTime) / (double)legacy.ResponseTime * 100;
    }
    
    private List<string> ExtractKeyData(string html)
    {
        var doc = new HtmlDocument();
        doc.LoadHtml(html);
        
        // Extract data from key elements (tables, lists, etc.)
        var data = new List<string>();
        
        var tables = doc.DocumentNode.SelectNodes("//table");
        if (tables != null)
        {
            foreach (var table in tables)
            {
                data.Add(table.InnerText.Trim());
            }
        }
        
        return data;
    }
    
    private byte[] TakeScreenshot(IWebDriver driver)
    {
        var screenshot = ((ITakesScreenshot)driver).GetScreenshot();
        return screenshot.AsByteArray;
    }
}

[TestFixture]
public class MigrationValidationTests
{
    private MigrationTestFramework _framework;
    
    [SetUp]
    public void Setup()
    {
        _framework = new MigrationTestFramework(
            "http://legacy.example.com", 
            "http://modern.example.com");
    }
    
    [Test]
    public async Task ProductSearch_Migration_ShouldProduceSameResults()
    {
        // Arrange
        var testData = new Dictionary<string, string>
        {
            { "txtSearchTerm", "laptop" },
            { "ddlCategory", "Electronics" }
        };
        
        // Act
        var result = await _framework.ComparePages("Search.aspx", testData);
        
        // Assert
        Assert.IsTrue(result.FunctionallyEquivalent, "Search results should be functionally equivalent");
        Assert.Greater(result.PerformanceImprovement, 0, "Performance should be improved");
        Assert.IsTrue(result.LegacyResult.Success);
        Assert.IsTrue(result.ModernResult.Success);
    }
}
```

## Test Automation Framework

### Comprehensive Test Automation

#### Test Configuration and Management
```csharp
public class TestConfiguration
{
    public string BaseUrl { get; set; }
    public string DatabaseConnectionString { get; set; }
    public string TestDataPath { get; set; }
    public int TimeoutSeconds { get; set; } = 30;
    public bool EnableScreenshots { get; set; } = true;
    public string ScreenshotPath { get; set; }
    public TestEnvironment Environment { get; set; }
}

public enum TestEnvironment
{
    Development,
    Testing,
    Staging,
    Production
}

public class TestManager
{
    private readonly TestConfiguration _config;
    private readonly IWebDriver _driver;
    private readonly TestDataManager _testDataManager;
    
    public TestManager(TestConfiguration config)
    {
        _config = config;
        _driver = CreateWebDriver();
        _testDataManager = new TestDataManager(config.TestDataPath);
    }
    
    private IWebDriver CreateWebDriver()
    {
        var options = new ChromeOptions();
        options.AddArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage");
        
        return new ChromeDriver(options);
    }
    
    public void Dispose()
    {
        _driver?.Quit();
    }
}

// Test data management
public class TestDataManager
{
    private readonly string _dataPath;
    private readonly Dictionary<string, object> _testData;
    
    public TestDataManager(string dataPath)
    {
        _dataPath = dataPath;
        _testData = LoadTestData();
    }
    
    private Dictionary<string, object> LoadTestData()
    {
        var jsonContent = File.ReadAllText(_dataPath);
        return JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonContent);
    }
    
    public T GetTestData<T>(string key)
    {
        if (_testData.TryGetValue(key, out var value))
        {
            return JsonConvert.DeserializeObject<T>(value.ToString());
        }
        
        throw new KeyNotFoundException($"Test data with key '{key}' not found");
    }
}

// Test reporting
public class TestReporter
{
    private readonly List<TestResult> _results = new List<TestResult>();
    
    public void LogTestResult(string testName, bool passed, string message = null, byte[] screenshot = null)
    {
        _results.Add(new TestResult
        {
            TestName = testName,
            Passed = passed,
            Message = message,
            Screenshot = screenshot,
            Timestamp = DateTime.Now
        });
    }
    
    public void GenerateReport(string outputPath)
    {
        var html = GenerateHtmlReport();
        File.WriteAllText(outputPath, html);
    }
    
    private string GenerateHtmlReport()
    {
        var sb = new StringBuilder();
        sb.AppendLine("<html><head><title>Test Results</title></head><body>");
        sb.AppendLine("<h1>WebForms Test Results</h1>");
        
        var passedCount = _results.Count(r => r.Passed);
        var failedCount = _results.Count(r => !r.Passed);
        
        sb.AppendLine($"<p>Total Tests: {_results.Count}</p>");
        sb.AppendLine($"<p>Passed: {passedCount}</p>");
        sb.AppendLine($"<p>Failed: {failedCount}</p>");
        
        foreach (var result in _results)
        {
            var status = result.Passed ? "PASS" : "FAIL";
            var color = result.Passed ? "green" : "red";
            
            sb.AppendLine($"<div style='border: 1px solid {color}; margin: 10px; padding: 10px;'>");
            sb.AppendLine($"<h3 style='color: {color};'>{status}: {result.TestName}</h3>");
            
            if (!string.IsNullOrEmpty(result.Message))
            {
                sb.AppendLine($"<p>{result.Message}</p>");
            }
            
            if (result.Screenshot != null)
            {
                var base64Image = Convert.ToBase64String(result.Screenshot);
                sb.AppendLine($"<img src='data:image/png;base64,{base64Image}' style='max-width: 500px;' />");
            }
            
            sb.AppendLine("</div>");
        }
        
        sb.AppendLine("</body></html>");
        return sb.ToString();
    }
}
```

This comprehensive testing strategy document provides frameworks and patterns for testing WebForms applications at all levels, from unit tests to end-to-end validation, including specific considerations for migration testing and performance validation.