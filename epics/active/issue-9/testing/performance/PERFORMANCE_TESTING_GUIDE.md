# WebForms Performance Testing Guide

## Overview
This guide provides comprehensive strategies for performance testing ASP.NET WebForms applications, addressing the unique performance characteristics and challenges inherent in the WebForms architecture.

## WebForms Performance Challenges

### 1. ViewState Overhead
ViewState can significantly impact page size and load times, especially in complex forms with many controls.

### 2. Page Lifecycle Overhead
The complex page lifecycle with multiple events can create performance bottlenecks.

### 3. Postback Model
Full page postbacks result in complete page reloads, affecting user experience and server load.

### 4. Session State Dependencies
Heavy reliance on session state can create memory pressure and scalability issues.

### 5. Control Hierarchy Rendering
Deep control hierarchies can slow down page rendering and increase memory usage.

## Performance Testing Framework

### 1. Base Performance Test Setup
```csharp
[TestClass]
public abstract class BasePerformanceTest
{
    protected PerformanceCounter _cpuCounter;
    protected PerformanceCounter _memoryCounter;
    protected Stopwatch _stopwatch;
    protected List<PerformanceMetric> _metrics;
    
    [TestInitialize]
    public virtual void Setup()
    {
        _cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
        _memoryCounter = new PerformanceCounter("Memory", "Available MBytes");
        _stopwatch = new Stopwatch();
        _metrics = new List<PerformanceMetric>();
        
        // Warm up performance counters
        _cpuCounter.NextValue();
        Thread.Sleep(1000);
    }
    
    [TestCleanup]
    public virtual void Cleanup()
    {
        _cpuCounter?.Dispose();
        _memoryCounter?.Dispose();
        
        // Log performance metrics
        LogMetrics();
    }
    
    protected void StartMeasurement(string operationName)
    {
        GC.Collect();
        GC.WaitForPendingFinalizers();
        GC.Collect();
        
        var metric = new PerformanceMetric
        {
            OperationName = operationName,
            StartTime = DateTime.UtcNow,
            StartMemory = GC.GetTotalMemory(false),
            StartCpu = _cpuCounter.NextValue()
        };
        
        _metrics.Add(metric);
        _stopwatch.Restart();
    }
    
    protected void EndMeasurement()
    {
        _stopwatch.Stop();
        
        var metric = _metrics.Last();
        metric.EndTime = DateTime.UtcNow;
        metric.Duration = _stopwatch.ElapsedMilliseconds;
        metric.EndMemory = GC.GetTotalMemory(false);
        metric.EndCpu = _cpuCounter.NextValue();
        metric.MemoryUsed = metric.EndMemory - metric.StartMemory;
    }
    
    private void LogMetrics()
    {
        foreach (var metric in _metrics)
        {
            TestContext.WriteLine($"Operation: {metric.OperationName}");
            TestContext.WriteLine($"Duration: {metric.Duration}ms");
            TestContext.WriteLine($"Memory Used: {metric.MemoryUsed / 1024}KB");
            TestContext.WriteLine($"CPU Usage: {metric.EndCpu - metric.StartCpu}%");
            TestContext.WriteLine("---");
        }
    }
    
    public TestContext TestContext { get; set; }
}

public class PerformanceMetric
{
    public string OperationName { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    public long Duration { get; set; }
    public long StartMemory { get; set; }
    public long EndMemory { get; set; }
    public long MemoryUsed { get; set; }
    public float StartCpu { get; set; }
    public float EndCpu { get; set; }
}
```

### 2. Page Load Performance Tests
```csharp
[TestClass]
public class PageLoadPerformanceTests : BasePerformanceTest
{
    private HttpClient _httpClient;
    private string _baseUrl = "http://localhost:8080";
    
    [TestInitialize]
    public override void Setup()
    {
        base.Setup();
        _httpClient = new HttpClient();
    }
    
    [TestCleanup]
    public override void Cleanup()
    {
        _httpClient?.Dispose();
        base.Cleanup();
    }
    
    [TestMethod]
    public async Task CustomerForm_InitialPageLoad_CompletesWithinPerformanceTargets()
    {
        // Arrange
        var targetLoadTime = 2000; // 2 seconds
        
        // Act
        StartMeasurement("Initial Page Load");
        var response = await _httpClient.GetAsync($"{_baseUrl}/CustomerForm.aspx");
        var content = await response.Content.ReadAsStringAsync();
        EndMeasurement();
        
        // Assert
        var metric = _metrics.Last();
        Assert.IsTrue(response.IsSuccessStatusCode, "Page should load successfully");
        Assert.IsTrue(metric.Duration < targetLoadTime, 
            $"Page load took {metric.Duration}ms, exceeding target of {targetLoadTime}ms");
        Assert.IsTrue(content.Contains("Customer Form"), "Page content should be loaded");
        
        // Check ViewState size
        var viewStateMatch = Regex.Match(content, @"id=""__VIEWSTATE"" value=""([^""]+)""");
        if (viewStateMatch.Success)
        {
            var viewStateSize = Convert.FromBase64String(viewStateMatch.Groups[1].Value).Length;
            Assert.IsTrue(viewStateSize < 50000, // 50KB limit
                $"ViewState size ({viewStateSize} bytes) exceeds recommended limit");
        }
    }
    
    [TestMethod]
    public async Task CustomerForm_PostbackPerformance_MeetsTargets()
    {
        // Arrange
        var targetPostbackTime = 1000; // 1 second
        
        // First, get the page to extract ViewState and form data
        var initialResponse = await _httpClient.GetAsync($"{_baseUrl}/CustomerForm.aspx");
        var initialContent = await initialResponse.Content.ReadAsStringAsync();
        
        var formData = ExtractFormData(initialContent);
        formData.Add("txtEmail", "perf@example.com");
        formData.Add("txtName", "Performance Test");
        formData.Add("btnSave", "Save Customer");
        
        // Act
        StartMeasurement("Form Postback");
        var postResponse = await _httpClient.PostAsync($"{_baseUrl}/CustomerForm.aspx", 
            new FormUrlEncodedContent(formData));
        var postContent = await postResponse.Content.ReadAsStringAsync();
        EndMeasurement();
        
        // Assert
        var metric = _metrics.Last();
        Assert.IsTrue(postResponse.IsSuccessStatusCode, "Postback should complete successfully");
        Assert.IsTrue(metric.Duration < targetPostbackTime, 
            $"Postback took {metric.Duration}ms, exceeding target of {targetPostbackTime}ms");
    }
    
    private Dictionary<string, string> ExtractFormData(string html)
    {
        var formData = new Dictionary<string, string>();
        
        // Extract ViewState
        var viewStateMatch = Regex.Match(html, @"id=""__VIEWSTATE"" value=""([^""]+)""");
        if (viewStateMatch.Success)
            formData.Add("__VIEWSTATE", viewStateMatch.Groups[1].Value);
        
        // Extract ViewStateGenerator
        var viewStateGenMatch = Regex.Match(html, @"id=""__VIEWSTATEGENERATOR"" value=""([^""]+)""");
        if (viewStateGenMatch.Success)
            formData.Add("__VIEWSTATEGENERATOR", viewStateGenMatch.Groups[1].Value);
        
        // Extract EventValidation
        var eventValidationMatch = Regex.Match(html, @"id=""__EVENTVALIDATION"" value=""([^""]+)""");
        if (eventValidationMatch.Success)
            formData.Add("__EVENTVALIDATION", eventValidationMatch.Groups[1].Value);
        
        return formData;
    }
}
```

### 3. Load Testing with NBomber
```csharp
[TestClass]
public class LoadPerformanceTests
{
    [TestMethod]
    public void CustomerForm_ConcurrentUsers_MaintainsPerformance()
    {
        var scenario = Scenario.Create("customer_form_load", async context =>
        {
            using var httpClient = new HttpClient();
            
            // Load initial page
            var response = await httpClient.GetAsync("http://localhost:8080/CustomerForm.aspx");
            
            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                
                // Extract form data and submit
                var formData = ExtractFormData(content);
                formData.Add("txtEmail", $"user{context.ScenarioInfo.ThreadId}@example.com");
                formData.Add("txtName", $"Load Test User {context.ScenarioInfo.ThreadId}");
                formData.Add("btnSave", "Save Customer");
                
                var postResponse = await httpClient.PostAsync("http://localhost:8080/CustomerForm.aspx", 
                    new FormUrlEncodedContent(formData));
                
                return postResponse.IsSuccessStatusCode ? Response.Ok() : Response.Fail();
            }
            
            return Response.Fail();
        })
        .WithLoadSimulations(
            Simulation.InjectPerSec(rate: 10, during: TimeSpan.FromMinutes(2)), // Ramp up
            Simulation.KeepConstant(copies: 50, during: TimeSpan.FromMinutes(5)), // Steady state
            Simulation.InjectPerSec(rate: 5, during: TimeSpan.FromMinutes(1))   // Ramp down
        );
        
        var stats = NBomberRunner
            .RegisterScenarios(scenario)
            .Run();
        
        // Assert performance targets
        var customerFormStats = stats.AllScenarioStats.First(s => s.ScenarioName == "customer_form_load");
        
        Assert.IsTrue(customerFormStats.Ok.Request.Mean < 2000, 
            $"Mean response time ({customerFormStats.Ok.Request.Mean}ms) exceeds target");
        Assert.IsTrue(customerFormStats.Ok.Request.Percentile95 < 5000, 
            $"95th percentile response time ({customerFormStats.Ok.Request.Percentile95}ms) exceeds target");
        Assert.IsTrue(customerFormStats.Fail.Request.Count == 0, 
            $"Found {customerFormStats.Fail.Request.Count} failed requests");
    }
    
    private Dictionary<string, string> ExtractFormData(string html)
    {
        // Same implementation as above
        var formData = new Dictionary<string, string>();
        
        var viewStateMatch = Regex.Match(html, @"id=""__VIEWSTATE"" value=""([^""]+)""");
        if (viewStateMatch.Success)
            formData.Add("__VIEWSTATE", viewStateMatch.Groups[1].Value);
        
        var viewStateGenMatch = Regex.Match(html, @"id=""__VIEWSTATEGENERATOR"" value=""([^""]+)""");
        if (viewStateGenMatch.Success)
            formData.Add("__VIEWSTATEGENERATOR", viewStateGenMatch.Groups[1].Value);
        
        var eventValidationMatch = Regex.Match(html, @"id=""__EVENTVALIDATION"" value=""([^""]+)""");
        if (eventValidationMatch.Success)
            formData.Add("__EVENTVALIDATION", eventValidationMatch.Groups[1].Value);
        
        return formData;
    }
}
```

### 4. Memory Performance Testing
```csharp
[TestClass]
public class MemoryPerformanceTests : BasePerformanceTest
{
    [TestMethod]
    public void CustomerService_ProcessManyCustomers_ManagesMemoryEfficiently()
    {
        // Arrange
        var customerService = new CustomerService();
        var customerCount = 10000;
        var maxMemoryIncrease = 50 * 1024 * 1024; // 50MB
        
        // Act
        StartMeasurement("Process Many Customers");
        
        for (int i = 0; i < customerCount; i++)
        {
            var request = new SaveCustomerRequest
            {
                Email = $"customer{i}@example.com",
                Name = $"Customer {i}",
                Phone = $"555-{i:D4}"
            };
            
            customerService.ValidateCustomer(request);
            
            // Force garbage collection every 1000 iterations
            if (i % 1000 == 0)
            {
                GC.Collect();
                GC.WaitForPendingFinalizers();
            }
        }
        
        EndMeasurement();
        
        // Assert
        var metric = _metrics.Last();
        Assert.IsTrue(metric.MemoryUsed < maxMemoryIncrease, 
            $"Memory usage ({metric.MemoryUsed / (1024 * 1024)}MB) exceeds limit ({maxMemoryIncrease / (1024 * 1024)}MB)");
    }
    
    [TestMethod]
    public void GridView_LargeDataset_DoesNotLeakMemory()
    {
        // Simulate loading large datasets in GridView
        var initialMemory = GC.GetTotalMemory(true);
        
        for (int iteration = 0; iteration < 10; iteration++)
        {
            StartMeasurement($"GridView Load Iteration {iteration}");
            
            // Simulate GridView data binding
            var customers = GenerateLargeCustomerDataset(5000);
            var dataTable = ConvertToDataTable(customers);
            
            // Simulate control tree creation and disposal
            SimulateGridViewBinding(dataTable);
            
            EndMeasurement();
            
            // Force cleanup
            customers = null;
            dataTable = null;
            GC.Collect();
            GC.WaitForPendingFinalizers();
        }
        
        var finalMemory = GC.GetTotalMemory(true);
        var memoryIncrease = finalMemory - initialMemory;
        
        Assert.IsTrue(memoryIncrease < 20 * 1024 * 1024, // 20MB limit
            $"Memory increased by {memoryIncrease / (1024 * 1024)}MB after multiple GridView operations");
    }
    
    private List<Customer> GenerateLargeCustomerDataset(int count)
    {
        return Enumerable.Range(1, count)
            .Select(i => new Customer
            {
                Id = i,
                Email = $"customer{i}@example.com",
                Name = $"Customer {i}",
                Phone = $"555-{i:D4}"
            })
            .ToList();
    }
    
    private DataTable ConvertToDataTable(List<Customer> customers)
    {
        var dataTable = new DataTable();
        dataTable.Columns.Add("Id", typeof(int));
        dataTable.Columns.Add("Email", typeof(string));
        dataTable.Columns.Add("Name", typeof(string));
        dataTable.Columns.Add("Phone", typeof(string));
        
        foreach (var customer in customers)
        {
            dataTable.Rows.Add(customer.Id, customer.Email, customer.Name, customer.Phone);
        }
        
        return dataTable;
    }
    
    private void SimulateGridViewBinding(DataTable data)
    {
        // Simulate the memory allocation that occurs during GridView binding
        var rows = new List<object[]>();
        
        foreach (DataRow row in data.Rows)
        {
            rows.Add(row.ItemArray);
        }
        
        // Simulate control creation overhead
        var controls = new List<Dictionary<string, object>>();
        foreach (var row in rows)
        {
            controls.Add(new Dictionary<string, object>
            {
                {"Text", row[1]}, // Email
                {"ToolTip", row[2]}, // Name
                {"CssClass", "grid-cell"}
            });
        }
    }
}
```

### 5. Database Performance Testing
```csharp
[TestClass]
public class DatabasePerformanceTests : BasePerformanceTest
{
    private string _connectionString;
    private ICustomerRepository _repository;
    
    [TestInitialize]
    public override void Setup()
    {
        base.Setup();
        _connectionString = ConfigurationManager.ConnectionStrings["TestDB"].ConnectionString;
        _repository = new CustomerRepository(_connectionString);
        
        // Setup test database with indexes
        SetupPerformanceTestDatabase();
    }
    
    [TestMethod]
    public void CustomerRepository_SaveManyCustomers_MeetsPerformanceTargets()
    {
        // Arrange
        var customerCount = 1000;
        var targetTimePerCustomer = 10; // 10ms per customer
        var customers = GenerateCustomers(customerCount);
        
        // Act
        StartMeasurement("Save Many Customers");
        
        foreach (var customer in customers)
        {
            _repository.Save(customer);
        }
        
        EndMeasurement();
        
        // Assert
        var metric = _metrics.Last();
        var avgTimePerCustomer = metric.Duration / customerCount;
        
        Assert.IsTrue(avgTimePerCustomer < targetTimePerCustomer, 
            $"Average save time ({avgTimePerCustomer}ms) exceeds target ({targetTimePerCustomer}ms)");
    }
    
    [TestMethod]
    public void CustomerRepository_SearchOperations_ReturnResultsQuickly()
    {
        // Arrange - seed database with test data
        SeedDatabaseWithTestData(10000);
        
        var searchQueries = new[]
        {
            "john@",
            "example.com",
            "Smith",
            "555-"
        };
        
        // Act & Assert
        foreach (var query in searchQueries)
        {
            StartMeasurement($"Search: {query}");
            
            var results = _repository.SearchCustomers(query);
            
            EndMeasurement();
            
            var metric = _metrics.Last();
            Assert.IsTrue(metric.Duration < 500, 
                $"Search for '{query}' took {metric.Duration}ms, exceeding 500ms target");
            Assert.IsTrue(results.Count > 0, $"Search for '{query}' should return results");
        }
    }
    
    [TestMethod]
    public void CustomerRepository_ConcurrentOperations_MaintainsPerformance()
    {
        var tasks = new List<Task>();
        var concurrentUsers = 20;
        var operationsPerUser = 50;
        var results = new ConcurrentBag<PerformanceResult>();
        
        // Act - simulate concurrent database operations
        for (int user = 0; user < concurrentUsers; user++)
        {
            var userId = user;
            tasks.Add(Task.Run(() =>
            {
                var userStopwatch = Stopwatch.StartNew();
                
                for (int op = 0; op < operationsPerUser; op++)
                {
                    var customer = new Customer
                    {
                        Email = $"user{userId}.op{op}@example.com",
                        Name = $"User {userId} Operation {op}",
                        Phone = $"555-{userId:D2}{op:D2}"
                    };
                    
                    var id = _repository.Save(customer);
                    var retrieved = _repository.GetById(id);
                    
                    Assert.IsNotNull(retrieved, "Should be able to retrieve saved customer");
                }
                
                userStopwatch.Stop();
                results.Add(new PerformanceResult
                {
                    UserId = userId,
                    TotalTime = userStopwatch.ElapsedMilliseconds,
                    Operations = operationsPerUser
                });
            }));
        }
        
        Task.WaitAll(tasks.ToArray());
        
        // Assert
        var avgTimePerOperation = results.Average(r => r.TotalTime / r.Operations);
        var maxTimePerOperation = results.Max(r => r.TotalTime / r.Operations);
        
        Assert.IsTrue(avgTimePerOperation < 20, 
            $"Average operation time ({avgTimePerOperation}ms) exceeds target (20ms)");
        Assert.IsTrue(maxTimePerOperation < 100, 
            $"Maximum operation time ({maxTimePerOperation}ms) exceeds target (100ms)");
    }
    
    private void SetupPerformanceTestDatabase()
    {
        using var connection = new SqlConnection(_connectionString);
        connection.Open();
        
        // Create indexes for performance
        var createIndexCommand = new SqlCommand(@"
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Customers_Email')
            CREATE INDEX IX_Customers_Email ON Customers(Email);
            
            IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Customers_Name')
            CREATE INDEX IX_Customers_Name ON Customers(Name);
        ", connection);
        
        createIndexCommand.ExecuteNonQuery();
    }
    
    private void SeedDatabaseWithTestData(int count)
    {
        var customers = GenerateCustomers(count);
        
        using var connection = new SqlConnection(_connectionString);
        connection.Open();
        
        using var transaction = connection.BeginTransaction();
        
        foreach (var customer in customers)
        {
            var command = new SqlCommand(
                "INSERT INTO Customers (Email, Name, Phone) VALUES (@Email, @Name, @Phone)", 
                connection, transaction);
            
            command.Parameters.AddWithValue("@Email", customer.Email);
            command.Parameters.AddWithValue("@Name", customer.Name);
            command.Parameters.AddWithValue("@Phone", customer.Phone);
            
            command.ExecuteNonQuery();
        }
        
        transaction.Commit();
    }
    
    private List<Customer> GenerateCustomers(int count)
    {
        var random = new Random();
        var firstNames = new[] { "John", "Jane", "Bob", "Alice", "Charlie", "Diana" };
        var lastNames = new[] { "Doe", "Smith", "Johnson", "Brown", "Wilson", "Garcia" };
        var domains = new[] { "example.com", "test.org", "sample.net" };
        
        return Enumerable.Range(1, count)
            .Select(i =>
            {
                var firstName = firstNames[random.Next(firstNames.Length)];
                var lastName = lastNames[random.Next(lastNames.Length)];
                var domain = domains[random.Next(domains.Length)];
                
                return new Customer
                {
                    Email = $"{firstName.ToLower()}.{lastName.ToLower()}.{i}@{domain}",
                    Name = $"{firstName} {lastName}",
                    Phone = $"555-{random.Next(100, 999)}-{random.Next(1000, 9999)}"
                };
            })
            .ToList();
    }
}

public class PerformanceResult
{
    public int UserId { get; set; }
    public long TotalTime { get; set; }
    public int Operations { get; set; }
}
```

### 6. ViewState Performance Analysis
```csharp
[TestClass]
public class ViewStatePerformanceTests
{
    [TestMethod]
    public void CustomerForm_ViewStateSize_StaysWithinLimits()
    {
        // Test different scenarios that affect ViewState size
        var scenarios = new[]
        {
            new { Name = "Empty Form", Controls = 0, ExpectedSizeKB = 5 },
            new { Name = "Basic Form", Controls = 10, ExpectedSizeKB = 15 },
            new { Name = "Complex Form", Controls = 50, ExpectedSizeKB = 50 },
            new { Name = "GridView Small", Controls = 100, ExpectedSizeKB = 100 },
            new { Name = "GridView Large", Controls = 500, ExpectedSizeKB = 250 }
        };
        
        foreach (var scenario in scenarios)
        {
            var viewStateSize = SimulateViewStateSize(scenario.Controls);
            var viewStateSizeKB = viewStateSize / 1024;
            
            Assert.IsTrue(viewStateSizeKB < scenario.ExpectedSizeKB, 
                $"{scenario.Name}: ViewState size ({viewStateSizeKB}KB) exceeds expected limit ({scenario.ExpectedSizeKB}KB)");
            
            TestContext.WriteLine($"{scenario.Name}: ViewState size = {viewStateSizeKB}KB");
        }
    }
    
    private long SimulateViewStateSize(int controlCount)
    {
        // Simulate ViewState generation based on control count
        var baseViewState = "ViewState data for page lifecycle";
        var controlViewState = string.Join("", Enumerable.Repeat("Control data", controlCount));
        var totalViewState = baseViewState + controlViewState;
        
        // Simulate compression and Base64 encoding
        var compressed = Compress(totalViewState);
        var base64 = Convert.ToBase64String(compressed);
        
        return base64.Length;
    }
    
    private byte[] Compress(string text)
    {
        var bytes = Encoding.UTF8.GetBytes(text);
        
        using var memoryStream = new MemoryStream();
        using (var gzipStream = new GZipStream(memoryStream, CompressionMode.Compress))
        {
            gzipStream.Write(bytes, 0, bytes.Length);
        }
        
        return memoryStream.ToArray();
    }
    
    public TestContext TestContext { get; set; }
}
```

## Real User Monitoring (RUM) Simulation

### 1. Browser Performance Testing
```csharp
[TestClass]
public class BrowserPerformanceTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        var options = new ChromeOptions();
        options.AddArgument("--enable-precise-memory-info");
        _driver = new ChromeDriver(options);
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_ClientSidePerformance_MeetsTargets()
    {
        // Navigate to page
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Measure page load performance
        var performanceMetrics = GetBrowserPerformanceMetrics();
        
        Assert.IsTrue(performanceMetrics.DomContentLoaded < 2000, 
            $"DOM content loaded time ({performanceMetrics.DomContentLoaded}ms) exceeds target");
        Assert.IsTrue(performanceMetrics.LoadComplete < 3000, 
            $"Page load time ({performanceMetrics.LoadComplete}ms) exceeds target");
        Assert.IsTrue(performanceMetrics.FirstPaint < 1500, 
            $"First paint time ({performanceMetrics.FirstPaint}ms) exceeds target");
    }
    
    [TestMethod]
    public void CustomerForm_PostbackPerformance_MeetsClientTargets()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Fill form
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys("perf@example.com");
        _driver.FindElement(By.CssSelector("input[id$='txtName']")).SendKeys("Performance Test");
        
        // Measure postback performance
        var startTime = GetCurrentTime();
        _driver.FindElement(By.CssSelector("input[id$='btnSave']")).Click();
        
        // Wait for postback completion
        var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(10));
        wait.Until(driver => driver.FindElement(By.CssSelector("span[id$='lblMessage']")).Displayed);
        
        var endTime = GetCurrentTime();
        var postbackTime = endTime - startTime;
        
        Assert.IsTrue(postbackTime < 2000, 
            $"Postback time ({postbackTime}ms) exceeds target (2000ms)");
    }
    
    private BrowserPerformanceMetrics GetBrowserPerformanceMetrics()
    {
        var script = @"
            return {
                domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                loadComplete: performance.timing.loadEventEnd - performance.timing.navigationStart,
                firstPaint: performance.getEntriesByType('paint').find(entry => entry.name === 'first-paint')?.startTime || 0
            };
        ";
        
        var result = (Dictionary<string, object>)((IJavaScriptExecutor)_driver).ExecuteScript(script);
        
        return new BrowserPerformanceMetrics
        {
            DomContentLoaded = Convert.ToInt64(result["domContentLoaded"]),
            LoadComplete = Convert.ToInt64(result["loadComplete"]),
            FirstPaint = Convert.ToInt64(result["firstPaint"])
        };
    }
    
    private long GetCurrentTime()
    {
        var script = "return performance.now();";
        return Convert.ToInt64(((IJavaScriptExecutor)_driver).ExecuteScript(script));
    }
}

public class BrowserPerformanceMetrics
{
    public long DomContentLoaded { get; set; }
    public long LoadComplete { get; set; }
    public long FirstPaint { get; set; }
}
```

## Performance Benchmarking and Reporting

### 1. Performance Report Generation
```csharp
public class PerformanceReportGenerator
{
    public void GenerateReport(List<PerformanceMetric> metrics, string outputPath)
    {
        var report = new StringBuilder();
        
        report.AppendLine("# WebForms Performance Test Report");
        report.AppendLine($"Generated: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss} UTC");
        report.AppendLine();
        
        // Summary statistics
        report.AppendLine("## Summary");
        report.AppendLine($"Total Operations: {metrics.Count}");
        report.AppendLine($"Average Duration: {metrics.Average(m => m.Duration):F2}ms");
        report.AppendLine($"Maximum Duration: {metrics.Max(m => m.Duration)}ms");
        report.AppendLine($"Total Memory Used: {metrics.Sum(m => m.MemoryUsed) / (1024 * 1024):F2}MB");
        report.AppendLine();
        
        // Detailed results
        report.AppendLine("## Detailed Results");
        report.AppendLine("| Operation | Duration (ms) | Memory (KB) | Status |");
        report.AppendLine("|-----------|---------------|-------------|--------|");
        
        foreach (var metric in metrics)
        {
            var status = GetPerformanceStatus(metric);
            report.AppendLine($"| {metric.OperationName} | {metric.Duration} | {metric.MemoryUsed / 1024:F1} | {status} |");
        }
        
        // Performance trends
        GeneratePerformanceTrends(metrics, report);
        
        File.WriteAllText(outputPath, report.ToString());
    }
    
    private string GetPerformanceStatus(PerformanceMetric metric)
    {
        if (metric.Duration < 1000 && metric.MemoryUsed < 10 * 1024 * 1024)
            return "✅ Good";
        else if (metric.Duration < 3000 && metric.MemoryUsed < 50 * 1024 * 1024)
            return "⚠️ Warning";
        else
            return "❌ Poor";
    }
    
    private void GeneratePerformanceTrends(List<PerformanceMetric> metrics, StringBuilder report)
    {
        report.AppendLine();
        report.AppendLine("## Performance Trends");
        
        var groupedMetrics = metrics.GroupBy(m => m.OperationName);
        
        foreach (var group in groupedMetrics)
        {
            var operationMetrics = group.OrderBy(m => m.StartTime).ToList();
            
            if (operationMetrics.Count > 1)
            {
                var trend = CalculateTrend(operationMetrics.Select(m => (double)m.Duration).ToList());
                var trendDirection = trend > 0 ? "📈 Increasing" : trend < 0 ? "📉 Decreasing" : "➡️ Stable";
                
                report.AppendLine($"- **{group.Key}**: {trendDirection} (slope: {trend:F3})");
            }
        }
    }
    
    private double CalculateTrend(List<double> values)
    {
        if (values.Count < 2) return 0;
        
        var n = values.Count;
        var sumX = Enumerable.Range(0, n).Sum();
        var sumY = values.Sum();
        var sumXY = values.Select((y, x) => x * y).Sum();
        var sumXX = Enumerable.Range(0, n).Select(x => x * x).Sum();
        
        return (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    }
}
```

## Performance Monitoring and Alerting

### 1. Continuous Performance Monitoring
```csharp
[TestClass]
public class ContinuousPerformanceMonitoring
{
    [TestMethod]
    public void PerformanceRegression_MonitoringTest()
    {
        var baseline = LoadPerformanceBaseline();
        var currentMetrics = RunPerformanceTests();
        
        var regressions = DetectRegressions(baseline, currentMetrics);
        
        if (regressions.Any())
        {
            var report = GenerateRegressionReport(regressions);
            File.WriteAllText("performance-regression-report.md", report);
            
            // In CI/CD, this would trigger alerts
            Assert.Fail($"Performance regressions detected:\n{report}");
        }
    }
    
    private Dictionary<string, double> LoadPerformanceBaseline()
    {
        // Load from previous test runs or configuration
        return new Dictionary<string, double>
        {
            {"PageLoad", 2000},
            {"FormSubmit", 1000},
            {"DatabaseQuery", 500},
            {"ViewStateSize", 50000}
        };
    }
    
    private Dictionary<string, double> RunPerformanceTests()
    {
        // Run actual performance tests and return metrics
        return new Dictionary<string, double>
        {
            {"PageLoad", MeasurePageLoad()},
            {"FormSubmit", MeasureFormSubmit()},
            {"DatabaseQuery", MeasureDatabaseQuery()},
            {"ViewStateSize", MeasureViewStateSize()}
        };
    }
    
    private List<PerformanceRegression> DetectRegressions(
        Dictionary<string, double> baseline, 
        Dictionary<string, double> current)
    {
        var regressions = new List<PerformanceRegression>();
        var threshold = 0.20; // 20% degradation threshold
        
        foreach (var metric in baseline)
        {
            if (current.ContainsKey(metric.Key))
            {
                var degradation = (current[metric.Key] - metric.Value) / metric.Value;
                
                if (degradation > threshold)
                {
                    regressions.Add(new PerformanceRegression
                    {
                        MetricName = metric.Key,
                        BaselineValue = metric.Value,
                        CurrentValue = current[metric.Key],
                        DegradationPercent = degradation * 100
                    });
                }
            }
        }
        
        return regressions;
    }
    
    private double MeasurePageLoad() => 1800; // Simulated
    private double MeasureFormSubmit() => 900; // Simulated
    private double MeasureDatabaseQuery() => 450; // Simulated
    private double MeasureViewStateSize() => 48000; // Simulated
    
    private string GenerateRegressionReport(List<PerformanceRegression> regressions)
    {
        var report = new StringBuilder();
        report.AppendLine("# Performance Regression Report");
        report.AppendLine();
        
        foreach (var regression in regressions)
        {
            report.AppendLine($"## {regression.MetricName}");
            report.AppendLine($"- Baseline: {regression.BaselineValue:F2}");
            report.AppendLine($"- Current: {regression.CurrentValue:F2}");
            report.AppendLine($"- Degradation: {regression.DegradationPercent:F1}%");
            report.AppendLine();
        }
        
        return report.ToString();
    }
}

public class PerformanceRegression
{
    public string MetricName { get; set; }
    public double BaselineValue { get; set; }
    public double CurrentValue { get; set; }
    public double DegradationPercent { get; set; }
}
```

## Best Practices Summary

### 1. Performance Testing Strategy
- **Establish Baselines**: Define performance targets for key metrics
- **Test Early and Often**: Include performance tests in CI/CD pipeline
- **Real-World Scenarios**: Test with realistic data volumes and user patterns
- **Monitor Trends**: Track performance over time to detect regressions
- **Environment Consistency**: Use consistent test environments

### 2. Key Performance Metrics
- **Page Load Time**: <2 seconds for initial load
- **Postback Time**: <1 second for form submissions
- **Database Queries**: <500ms for typical operations
- **ViewState Size**: <50KB for complex forms
- **Memory Usage**: Stable across multiple operations
- **Concurrent Users**: Support target user load

### 3. Performance Optimization Areas
- **ViewState Management**: Disable where not needed, use control state
- **AJAX Implementation**: Use UpdatePanels selectively
- **Database Optimization**: Proper indexing and query optimization
- **Caching Strategy**: Output caching, data caching
- **Resource Bundling**: Combine CSS/JavaScript files
- **Image Optimization**: Compress and properly size images

### 4. Testing Tools and Frameworks
- **Load Testing**: NBomber, Apache JMeter
- **Profiling**: dotMemory, PerfView
- **Browser Testing**: Selenium WebDriver, Playwright
- **Database Testing**: SQL Server Profiler, Query Store
- **Monitoring**: Application Insights, Custom counters

This comprehensive performance testing guide ensures WebForms applications meet performance requirements and maintain optimal user experience under various load conditions.