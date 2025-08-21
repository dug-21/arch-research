# WebForms Code Examples - Patterns and Anti-Patterns

## Critical Code Pattern Examples

### 1. ViewState Bloat Example

#### Problematic ViewState Usage
```csharp
public partial class CustomerManager : Page
{
    // This creates massive ViewState - BAD PRACTICE
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadCustomerList(); // Loads 1000+ customers into ViewState
        }
    }
    
    private void LoadCustomerList()
    {
        // This will be stored in ViewState on every postback
        var customers = CustomerService.GetAllCustomers(); // 1000+ records
        GridView1.DataSource = customers;
        GridView1.DataBind();
        
        // ViewState now contains entire customer list
        // Hidden field can reach 500KB+ in size
    }
    
    protected void AddCustomer_Click(object sender, EventArgs e)
    {
        // Every postback carries 500KB+ ViewState payload
        var newCustomer = new Customer
        {
            Name = NameTextBox.Text,
            Email = EmailTextBox.Text
        };
        
        CustomerService.AddCustomer(newCustomer);
        
        // Reload entire list again - ViewState doubles in size
        LoadCustomerList();
    }
}
```

#### Better Approach
```csharp
public partial class CustomerManagerImproved : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        // Disable ViewState for read-only data
        GridView1.EnableViewState = false;
        
        if (!IsPostBack)
        {
            LoadCustomerList();
        }
    }
    
    private void LoadCustomerList()
    {
        // Use paging to limit data
        var customers = CustomerService.GetCustomers(pageIndex: 0, pageSize: 25);
        GridView1.DataSource = customers;
        GridView1.DataBind();
        
        // Store only page index in ViewState, not data
        ViewState["CurrentPage"] = 0;
    }
}
```

### 2. Massive Code-Behind Anti-Pattern

#### Problematic Monolithic Code-Behind
```csharp
public partial class OrderManagement : Page
{
    // 2000+ line code-behind file with everything mixed together
    
    protected void Page_Load(object sender, EventArgs e)
    {
        // 200 lines of mixed UI logic, validation, and business rules
        if (!IsPostBack)
        {
            // Direct database access in Page_Load
            string connectionString = ConfigurationManager.ConnectionStrings["DB"].ConnectionString;
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                string sql = @"
                    SELECT o.OrderID, o.OrderDate, c.CustomerName, 
                           od.ProductID, p.ProductName, od.Quantity, od.UnitPrice
                    FROM Orders o 
                    INNER JOIN Customers c ON o.CustomerID = c.CustomerID
                    INNER JOIN OrderDetails od ON o.OrderID = od.OrderID
                    INNER JOIN Products p ON od.ProductID = p.ProductID
                    WHERE o.OrderDate >= DATEADD(month, -3, GETDATE())
                    ORDER BY o.OrderDate DESC";
                
                SqlCommand cmd = new SqlCommand(sql, conn);
                conn.Open();
                
                // Complex data manipulation in UI layer
                SqlDataReader reader = cmd.ExecuteReader();
                var orders = new List<OrderViewModel>();
                
                while (reader.Read())
                {
                    // Complex business logic mixed with data access
                    var order = new OrderViewModel
                    {
                        OrderID = (int)reader["OrderID"],
                        OrderDate = (DateTime)reader["OrderDate"],
                        CustomerName = reader["CustomerName"].ToString(),
                        ProductName = reader["ProductName"].ToString(),
                        Quantity = (int)reader["Quantity"],
                        UnitPrice = (decimal)reader["UnitPrice"],
                        // Calculate total with tax logic in UI layer
                        Total = CalculateOrderTotal((int)reader["Quantity"], (decimal)reader["UnitPrice"])
                    };
                    orders.Add(order);
                }
                
                GridView1.DataSource = orders;
                GridView1.DataBind();
            }
            
            // More business logic mixed in
            ApplyUserPermissions();
            ValidateInventoryLevels();
            UpdateDashboardMetrics();
        }
    }
    
    protected void GridView1_RowEditing(object sender, GridViewEditEventArgs e)
    {
        // 150 lines of editing logic with embedded business rules
        GridView1.EditIndex = e.NewEditIndex;
        
        // Direct database manipulation
        string orderID = GridView1.DataKeys[e.NewEditIndex].Value.ToString();
        
        // Load order details with complex joins
        string connectionString = ConfigurationManager.ConnectionStrings["DB"].ConnectionString;
        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            // More embedded SQL and business logic...
        }
    }
    
    protected void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
    {
        // 300 lines of update logic with validation
        // Mixed validation, business rules, and data access
        
        GridViewRow row = GridView1.Rows[e.RowIndex];
        string orderID = GridView1.DataKeys[e.RowIndex].Value.ToString();
        
        // Inline validation (should be in business layer)
        TextBox quantityTextBox = (TextBox)row.FindControl("QuantityTextBox");
        if (!int.TryParse(quantityTextBox.Text, out int quantity) || quantity <= 0)
        {
            // Error handling mixed with UI logic
            Label errorLabel = (Label)row.FindControl("ErrorLabel");
            errorLabel.Text = "Invalid quantity";
            errorLabel.ForeColor = Color.Red;
            return;
        }
        
        // Business rule validation in UI layer
        if (quantity > GetAvailableInventory(orderID))
        {
            // More inline error handling...
            return;
        }
        
        // Direct database update
        string updateSql = "UPDATE OrderDetails SET Quantity = @quantity WHERE OrderID = @orderID";
        using (SqlConnection conn = new SqlConnection(ConfigurationManager.ConnectionStrings["DB"].ConnectionString))
        {
            SqlCommand cmd = new SqlCommand(updateSql, conn);
            cmd.Parameters.AddWithValue("@quantity", quantity);
            cmd.Parameters.AddWithValue("@orderID", orderID);
            
            conn.Open();
            cmd.ExecuteNonQuery();
        }
        
        // Recalculate totals (business logic in UI)
        UpdateOrderTotals(orderID);
        
        // Audit logging in UI layer
        LogOrderUpdate(orderID, quantity);
        
        GridView1.EditIndex = -1;
        LoadOrderData(); // Reload everything
    }
    
    private decimal CalculateOrderTotal(int quantity, decimal unitPrice)
    {
        // Business logic that should be in service layer
        decimal subtotal = quantity * unitPrice;
        decimal taxRate = GetTaxRateForCustomer(); // Another database call
        decimal tax = subtotal * taxRate;
        decimal shipping = CalculateShipping(quantity); // More business logic
        
        return subtotal + tax + shipping;
    }
    
    private void ApplyUserPermissions()
    {
        // Authorization logic mixed in UI
        // 50+ lines of permission checking
    }
    
    private void ValidateInventoryLevels()
    {
        // Business validation in UI layer
        // 75+ lines of inventory checking
    }
    
    // ... 1500+ more lines of mixed responsibilities
}
```

#### Better Separation of Concerns
```csharp
// Service Layer
public class OrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly ICustomerService _customerService;
    private readonly IInventoryService _inventoryService;
    private readonly ITaxCalculator _taxCalculator;
    
    public OrderService(
        IOrderRepository orderRepository,
        ICustomerService customerService,
        IInventoryService inventoryService,
        ITaxCalculator taxCalculator)
    {
        _orderRepository = orderRepository;
        _customerService = customerService;
        _inventoryService = inventoryService;
        _taxCalculator = taxCalculator;
    }
    
    public async Task<List<OrderViewModel>> GetRecentOrdersAsync(int pageIndex, int pageSize)
    {
        var orders = await _orderRepository.GetRecentOrdersAsync(pageIndex, pageSize);
        return orders.Select(MapToViewModel).ToList();
    }
    
    public async Task<OrderUpdateResult> UpdateOrderQuantityAsync(int orderID, int newQuantity, string userID)
    {
        // Business validation
        var validationResult = await ValidateQuantityUpdateAsync(orderID, newQuantity);
        if (!validationResult.IsValid)
        {
            return OrderUpdateResult.Failed(validationResult.Errors);
        }
        
        // Authorization check
        if (!await CanUserModifyOrderAsync(userID, orderID))
        {
            return OrderUpdateResult.Failed("Insufficient permissions");
        }
        
        // Business logic
        await _orderRepository.UpdateQuantityAsync(orderID, newQuantity);
        await _inventoryService.AdjustInventoryAsync(orderID, newQuantity);
        
        return OrderUpdateResult.Success();
    }
}

// Improved Page Code-Behind
public partial class OrderManagementImproved : Page
{
    private OrderService _orderService;
    
    protected void Page_Load(object sender, EventArgs e)
    {
        _orderService = new OrderService(/* dependencies */);
        
        if (!IsPostBack)
        {
            LoadOrderData();
        }
    }
    
    private async void LoadOrderData()
    {
        try
        {
            var orders = await _orderService.GetRecentOrdersAsync(0, 25);
            GridView1.DataSource = orders;
            GridView1.DataBind();
        }
        catch (Exception ex)
        {
            // Proper error handling
            Logger.LogError(ex, "Failed to load order data");
            ErrorPanel.Visible = true;
            ErrorLabel.Text = "Unable to load orders. Please try again.";
        }
    }
    
    protected async void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
    {
        try
        {
            GridViewRow row = GridView1.Rows[e.RowIndex];
            int orderID = (int)GridView1.DataKeys[e.RowIndex].Value;
            
            TextBox quantityTextBox = (TextBox)row.FindControl("QuantityTextBox");
            if (!int.TryParse(quantityTextBox.Text, out int quantity))
            {
                ShowError("Invalid quantity format");
                return;
            }
            
            string userID = HttpContext.Current.User.Identity.Name;
            var result = await _orderService.UpdateOrderQuantityAsync(orderID, quantity, userID);
            
            if (result.IsSuccess)
            {
                GridView1.EditIndex = -1;
                LoadOrderData();
                ShowSuccess("Order updated successfully");
            }
            else
            {
                ShowError(result.ErrorMessage);
            }
        }
        catch (Exception ex)
        {
            Logger.LogError(ex, "Failed to update order");
            ShowError("Update failed. Please try again.");
        }
    }
}
```

### 3. Security Vulnerability Examples

#### SQL Injection Vulnerability
```csharp
protected void SearchCustomers_Click(object sender, EventArgs e)
{
    // CRITICAL VULNERABILITY - SQL Injection
    string customerName = CustomerNameTextBox.Text;
    string email = EmailTextBox.Text;
    
    string sql = $@"
        SELECT CustomerID, Name, Email, Phone 
        FROM Customers 
        WHERE Name LIKE '%{customerName}%' 
        AND Email LIKE '%{email}%'";
    
    // Attacker could input: '; DROP TABLE Customers; --
    // Resulting SQL: SELECT ... WHERE Name LIKE '%'; DROP TABLE Customers; --%'
    
    using (SqlConnection conn = new SqlConnection(ConnectionString))
    {
        SqlCommand cmd = new SqlCommand(sql, conn);
        conn.Open();
        
        GridView1.DataSource = cmd.ExecuteReader();
        GridView1.DataBind();
    }
}
```

#### Secure Version
```csharp
protected void SearchCustomers_Click(object sender, EventArgs e)
{
    string customerName = CustomerNameTextBox.Text?.Trim();
    string email = EmailTextBox.Text?.Trim();
    
    // Input validation
    if (string.IsNullOrEmpty(customerName) && string.IsNullOrEmpty(email))
    {
        ShowError("Please provide search criteria");
        return;
    }
    
    // Parameterized query prevents SQL injection
    string sql = @"
        SELECT CustomerID, Name, Email, Phone 
        FROM Customers 
        WHERE (@customerName IS NULL OR Name LIKE '%' + @customerName + '%')
        AND (@email IS NULL OR Email LIKE '%' + @email + '%')";
    
    using (SqlConnection conn = new SqlConnection(ConnectionString))
    {
        SqlCommand cmd = new SqlCommand(sql, conn);
        cmd.Parameters.AddWithValue("@customerName", 
            string.IsNullOrEmpty(customerName) ? (object)DBNull.Value : customerName);
        cmd.Parameters.AddWithValue("@email", 
            string.IsNullOrEmpty(email) ? (object)DBNull.Value : email);
        
        conn.Open();
        GridView1.DataSource = cmd.ExecuteReader();
        GridView1.DataBind();
    }
}
```

### 4. Testability Anti-Pattern

#### Untestable Code
```csharp
public partial class PaymentProcessor : Page
{
    protected void ProcessPayment_Click(object sender, EventArgs e)
    {
        // Impossible to unit test due to dependencies
        decimal amount = decimal.Parse(AmountTextBox.Text);
        string cardNumber = CardNumberTextBox.Text;
        string expiryDate = ExpiryDateTextBox.Text;
        
        // Direct dependency on HttpContext
        string userID = HttpContext.Current.User.Identity.Name;
        string sessionID = Session.SessionID;
        
        // Direct database access
        string connectionString = ConfigurationManager.ConnectionStrings["DB"].ConnectionString;
        using (SqlConnection conn = new SqlConnection(connectionString))
        {
            // Business logic mixed with data access
            string sql = "INSERT INTO Payments (UserID, Amount, CardNumber, Status) VALUES (@userID, @amount, @cardNumber, 'Pending')";
            SqlCommand cmd = new SqlCommand(sql, conn);
            cmd.Parameters.AddWithValue("@userID", userID);
            cmd.Parameters.AddWithValue("@amount", amount);
            cmd.Parameters.AddWithValue("@cardNumber", cardNumber);
            
            conn.Open();
            int paymentID = (int)cmd.ExecuteScalar();
            
            // External service call with no abstraction
            var paymentGateway = new PaymentGateway();
            var result = paymentGateway.ProcessPayment(cardNumber, amount, expiryDate);
            
            if (result.IsSuccess)
            {
                // Update database directly
                string updateSql = "UPDATE Payments SET Status = 'Completed', TransactionID = @transactionID WHERE PaymentID = @paymentID";
                SqlCommand updateCmd = new SqlCommand(updateSql, conn);
                updateCmd.Parameters.AddWithValue("@transactionID", result.TransactionID);
                updateCmd.Parameters.AddWithValue("@paymentID", paymentID);
                updateCmd.ExecuteNonQuery();
                
                // UI manipulation
                StatusLabel.Text = "Payment processed successfully";
                StatusLabel.ForeColor = Color.Green;
                Response.Redirect("PaymentSuccess.aspx");
            }
            else
            {
                // Error handling mixed with UI
                StatusLabel.Text = "Payment failed: " + result.ErrorMessage;
                StatusLabel.ForeColor = Color.Red;
            }
        }
    }
}
```

#### Testable Version
```csharp
// Business Logic Layer (Testable)
public class PaymentService
{
    private readonly IPaymentRepository _paymentRepository;
    private readonly IPaymentGateway _paymentGateway;
    private readonly IUserContext _userContext;
    
    public PaymentService(
        IPaymentRepository paymentRepository,
        IPaymentGateway paymentGateway,
        IUserContext userContext)
    {
        _paymentRepository = paymentRepository;
        _paymentGateway = paymentGateway;
        _userContext = userContext;
    }
    
    public async Task<PaymentResult> ProcessPaymentAsync(PaymentRequest request)
    {
        // Input validation
        var validationResult = ValidatePaymentRequest(request);
        if (!validationResult.IsValid)
        {
            return PaymentResult.Failed(validationResult.Errors);
        }
        
        // Create payment record
        var payment = new Payment
        {
            UserID = _userContext.UserID,
            Amount = request.Amount,
            CardNumber = MaskCardNumber(request.CardNumber),
            Status = PaymentStatus.Pending
        };
        
        var paymentID = await _paymentRepository.CreatePaymentAsync(payment);
        
        try
        {
            // Process payment through gateway
            var gatewayResult = await _paymentGateway.ProcessPaymentAsync(
                request.CardNumber, 
                request.Amount, 
                request.ExpiryDate);
            
            if (gatewayResult.IsSuccess)
            {
                await _paymentRepository.UpdatePaymentStatusAsync(
                    paymentID, 
                    PaymentStatus.Completed, 
                    gatewayResult.TransactionID);
                
                return PaymentResult.Success(paymentID, gatewayResult.TransactionID);
            }
            else
            {
                await _paymentRepository.UpdatePaymentStatusAsync(
                    paymentID, 
                    PaymentStatus.Failed, 
                    errorMessage: gatewayResult.ErrorMessage);
                
                return PaymentResult.Failed(gatewayResult.ErrorMessage);
            }
        }
        catch (Exception ex)
        {
            await _paymentRepository.UpdatePaymentStatusAsync(
                paymentID, 
                PaymentStatus.Error, 
                errorMessage: ex.Message);
            
            throw; // Re-throw for logging at higher level
        }
    }
}

// Unit Test Example
[Test]
public async Task ProcessPaymentAsync_ValidRequest_ReturnsSuccess()
{
    // Arrange
    var mockRepository = new Mock<IPaymentRepository>();
    var mockGateway = new Mock<IPaymentGateway>();
    var mockUserContext = new Mock<IUserContext>();
    
    mockUserContext.Setup(x => x.UserID).Returns("user123");
    mockRepository.Setup(x => x.CreatePaymentAsync(It.IsAny<Payment>()))
               .ReturnsAsync(12345);
    mockGateway.Setup(x => x.ProcessPaymentAsync(It.IsAny<string>(), It.IsAny<decimal>(), It.IsAny<string>()))
               .ReturnsAsync(new GatewayResult { IsSuccess = true, TransactionID = "txn123" });
    
    var service = new PaymentService(mockRepository.Object, mockGateway.Object, mockUserContext.Object);
    var request = new PaymentRequest
    {
        Amount = 100.00m,
        CardNumber = "4111111111111111",
        ExpiryDate = "12/25"
    };
    
    // Act
    var result = await service.ProcessPaymentAsync(request);
    
    // Assert
    Assert.IsTrue(result.IsSuccess);
    Assert.AreEqual("txn123", result.TransactionID);
    
    mockRepository.Verify(x => x.UpdatePaymentStatusAsync(
        12345, 
        PaymentStatus.Completed, 
        "txn123"), Times.Once);
}

// Page Code-Behind (Thin UI Layer)
public partial class PaymentProcessorImproved : Page
{
    private PaymentService _paymentService;
    
    protected void Page_Load(object sender, EventArgs e)
    {
        // Dependency injection would be better
        _paymentService = ServiceLocator.Get<PaymentService>();
    }
    
    protected async void ProcessPayment_Click(object sender, EventArgs e)
    {
        try
        {
            if (!ValidateInput())
            {
                return;
            }
            
            var request = new PaymentRequest
            {
                Amount = decimal.Parse(AmountTextBox.Text),
                CardNumber = CardNumberTextBox.Text,
                ExpiryDate = ExpiryDateTextBox.Text
            };
            
            var result = await _paymentService.ProcessPaymentAsync(request);
            
            if (result.IsSuccess)
            {
                Response.Redirect($"PaymentSuccess.aspx?id={result.PaymentID}");
            }
            else
            {
                ShowError(result.ErrorMessage);
            }
        }
        catch (Exception ex)
        {
            Logger.LogError(ex, "Payment processing failed");
            ShowError("Payment processing failed. Please try again.");
        }
    }
}
```

### 5. Performance Anti-Pattern Examples

#### Inefficient Data Loading
```csharp
protected void Page_Load(object sender, EventArgs e)
{
    // PERFORMANCE KILLER - Loading massive datasets
    var allCustomers = CustomerService.GetAllCustomers(); // 50,000+ records
    var allOrders = OrderService.GetAllOrders(); // 100,000+ records
    var allProducts = ProductService.GetAllProducts(); // 10,000+ records
    
    // Storing everything in ViewState
    ViewState["Customers"] = allCustomers;
    ViewState["Orders"] = allOrders;
    ViewState["Products"] = allProducts;
    
    // ViewState now 10MB+ causing massive page bloat
    // Every postback carries this massive payload
    
    // Inefficient nested loops
    foreach (var customer in allCustomers)
    {
        foreach (var order in allOrders)
        {
            if (order.CustomerID == customer.CustomerID)
            {
                foreach (var product in allProducts)
                {
                    // O(n³) complexity - extremely slow
                    if (order.ProductID == product.ProductID)
                    {
                        // Process order item
                    }
                }
            }
        }
    }
}
```

#### Optimized Version
```csharp
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        LoadCustomerPage(0, 25); // Paged loading
    }
}

private void LoadCustomerPage(int pageIndex, int pageSize)
{
    // Efficient paging query
    var customersPage = CustomerService.GetCustomersPage(pageIndex, pageSize);
    
    // Disable ViewState for read-only data
    CustomerGridView.EnableViewState = false;
    CustomerGridView.DataSource = customersPage.Data;
    CustomerGridView.DataBind();
    
    // Store only pagination info
    ViewState["CurrentPage"] = pageIndex;
    ViewState["TotalPages"] = customersPage.TotalPages;
}
```

## Summary of Critical Issues

### High Priority Code Issues:
1. **ViewState Bloat** - Can reach MBs causing performance degradation
2. **SQL Injection Vulnerabilities** - Direct string concatenation in queries
3. **Massive Code-Behind Files** - Mixed responsibilities, poor maintainability
4. **Poor Testability** - Tight coupling to framework dependencies
5. **Performance Anti-Patterns** - Inefficient data loading and processing

### Immediate Remediation Steps:
1. Implement parameterized queries
2. Extract business logic from code-behind
3. Disable ViewState where appropriate
4. Implement proper error handling
5. Add input validation and sanitization

### Long-term Migration Strategy:
1. Adopt MVP/MVVM patterns
2. Implement dependency injection
3. Plan migration to ASP.NET Core
4. Establish unit testing practices
5. Implement proper security measures

---
*Code examples compiled by WebForms Code Analyzer Agent*
*Part of comprehensive Hive Mind assessment*