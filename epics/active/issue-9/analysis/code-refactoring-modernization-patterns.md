# WebForms Code Refactoring and Modernization Patterns

## Overview

This guide provides comprehensive patterns for refactoring WebForms code to modern standards while maintaining functionality and improving maintainability, testability, and performance.

## Separation of Concerns Refactoring

### Code-Behind Extraction Pattern

**Before: Tightly Coupled WebForms**
```csharp
public partial class ProductList : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadCategories();
            LoadProducts();
        }
    }
    
    private void LoadCategories()
    {
        using (var conn = new SqlConnection(ConfigurationManager.ConnectionStrings["DB"].ConnectionString))
        {
            conn.Open();
            var cmd = new SqlCommand("SELECT Id, Name FROM Categories", conn);
            var reader = cmd.ExecuteReader();
            
            ddlCategory.Items.Clear();
            ddlCategory.Items.Add(new ListItem("All Categories", "0"));
            
            while (reader.Read())
            {
                ddlCategory.Items.Add(new ListItem(reader["Name"].ToString(), reader["Id"].ToString()));
            }
        }
    }
    
    private void LoadProducts()
    {
        using (var conn = new SqlConnection(ConfigurationManager.ConnectionStrings["DB"].ConnectionString))
        {
            conn.Open();
            var sql = "SELECT Id, Name, Price, CategoryId FROM Products";
            var cmd = new SqlCommand(sql, conn);
            
            var dt = new DataTable();
            var adapter = new SqlDataAdapter(cmd);
            adapter.Fill(dt);
            
            GridView1.DataSource = dt;
            GridView1.DataBind();
        }
    }
    
    protected void ddlCategory_SelectedIndexChanged(object sender, EventArgs e)
    {
        int categoryId = Convert.ToInt32(ddlCategory.SelectedValue);
        
        using (var conn = new SqlConnection(ConfigurationManager.ConnectionStrings["DB"].ConnectionString))
        {
            conn.Open();
            var sql = categoryId == 0 
                ? "SELECT Id, Name, Price, CategoryId FROM Products"
                : "SELECT Id, Name, Price, CategoryId FROM Products WHERE CategoryId = @CategoryId";
                
            var cmd = new SqlCommand(sql, conn);
            if (categoryId > 0)
                cmd.Parameters.AddWithValue("@CategoryId", categoryId);
            
            var dt = new DataTable();
            var adapter = new SqlDataAdapter(cmd);
            adapter.Fill(dt);
            
            GridView1.DataSource = dt;
            GridView1.DataBind();
        }
    }
}
```

**After: Separated Concerns**
```csharp
// Data Access Layer
public interface IProductRepository
{
    Task<List<Product>> GetProductsAsync();
    Task<List<Product>> GetProductsByCategoryAsync(int categoryId);
    Task<Product> GetProductByIdAsync(int id);
}

public class ProductRepository : IProductRepository
{
    private readonly string _connectionString;
    
    public ProductRepository(string connectionString)
    {
        _connectionString = connectionString;
    }
    
    public async Task<List<Product>> GetProductsAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        var sql = "SELECT Id, Name, Price, CategoryId FROM Products";
        return (await connection.QueryAsync<Product>(sql)).ToList();
    }
    
    public async Task<List<Product>> GetProductsByCategoryAsync(int categoryId)
    {
        using var connection = new SqlConnection(_connectionString);
        var sql = "SELECT Id, Name, Price, CategoryId FROM Products WHERE CategoryId = @CategoryId";
        return (await connection.QueryAsync<Product>(sql, new { CategoryId = categoryId })).ToList();
    }
}

// Business Logic Layer
public interface ICategoryService
{
    Task<List<Category>> GetCategoriesAsync();
}

public interface IProductService
{
    Task<List<Product>> GetProductsAsync();
    Task<List<Product>> GetProductsByCategoryAsync(int categoryId);
}

public class ProductService : IProductService
{
    private readonly IProductRepository _repository;
    private readonly ILogger<ProductService> _logger;
    
    public ProductService(IProductRepository repository, ILogger<ProductService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    public async Task<List<Product>> GetProductsAsync()
    {
        try
        {
            return await _repository.GetProductsAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to retrieve products");
            throw new ServiceException("Unable to retrieve products", ex);
        }
    }
    
    public async Task<List<Product>> GetProductsByCategoryAsync(int categoryId)
    {
        if (categoryId <= 0)
            return await GetProductsAsync();
            
        return await _repository.GetProductsByCategoryAsync(categoryId);
    }
}

// Presentation Layer (WebForms Page)
public partial class ProductList : Page
{
    private readonly ICategoryService _categoryService;
    private readonly IProductService _productService;
    
    // Dependency injection in WebForms (using constructor injection via custom PageFactory)
    public ProductList(ICategoryService categoryService, IProductService productService)
    {
        _categoryService = categoryService;
        _productService = productService;
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadCategoriesAsync();
            await LoadProductsAsync();
        }
    }
    
    private async Task LoadCategoriesAsync()
    {
        try
        {
            var categories = await _categoryService.GetCategoriesAsync();
            
            ddlCategory.Items.Clear();
            ddlCategory.Items.Add(new ListItem("All Categories", "0"));
            
            foreach (var category in categories)
            {
                ddlCategory.Items.Add(new ListItem(category.Name, category.Id.ToString()));
            }
        }
        catch (Exception ex)
        {
            ShowErrorMessage("Failed to load categories");
            // Log error
        }
    }
    
    private async Task LoadProductsAsync(int categoryId = 0)
    {
        try
        {
            var products = categoryId == 0 
                ? await _productService.GetProductsAsync()
                : await _productService.GetProductsByCategoryAsync(categoryId);
                
            GridView1.DataSource = products;
            GridView1.DataBind();
        }
        catch (Exception ex)
        {
            ShowErrorMessage("Failed to load products");
            // Log error
        }
    }
    
    protected async void ddlCategory_SelectedIndexChanged(object sender, EventArgs e)
    {
        int categoryId = Convert.ToInt32(ddlCategory.SelectedValue);
        await LoadProductsAsync(categoryId);
    }
    
    private void ShowErrorMessage(string message)
    {
        // Display error message to user
        lblError.Text = message;
        lblError.Visible = true;
    }
}
```

## ViewState Elimination Patterns

### State Management Refactoring
```csharp
// Before: Heavy ViewState Usage
public partial class OrderManagement : Page
{
    private List<Order> _orders;
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (ViewState["Orders"] != null)
        {
            _orders = (List<Order>)ViewState["Orders"];
        }
        
        if (!IsPostBack)
        {
            LoadOrders();
            ViewState["Orders"] = _orders;
        }
    }
    
    protected void GridView_PageIndexChanging(object sender, GridViewPageEventArgs e)
    {
        GridView1.PageIndex = e.NewPageIndex;
        _orders = (List<Order>)ViewState["Orders"];
        BindGrid();
    }
    
    protected void GridView_Sorting(object sender, GridViewSortEventArgs e)
    {
        _orders = (List<Order>)ViewState["Orders"];
        
        if (ViewState["SortDirection"] != null && ViewState["SortExpression"].ToString() == e.SortExpression)
        {
            var sortDirection = (SortDirection)ViewState["SortDirection"];
            e.SortDirection = sortDirection == SortDirection.Ascending ? SortDirection.Descending : SortDirection.Ascending;
        }
        
        ViewState["SortDirection"] = e.SortDirection;
        ViewState["SortExpression"] = e.SortExpression;
        
        SortOrders(e.SortExpression, e.SortDirection);
        BindGrid();
    }
}

// After: Stateless with Repository Pattern
public partial class OrderManagement : Page
{
    private readonly IOrderService _orderService;
    
    // Page state properties
    protected int CurrentPage 
    { 
        get => ViewState["CurrentPage"] as int? ?? 0; 
        set => ViewState["CurrentPage"] = value; 
    }
    
    protected string SortExpression 
    { 
        get => ViewState["SortExpression"] as string ?? "OrderDate"; 
        set => ViewState["SortExpression"] = value; 
    }
    
    protected SortDirection SortDirection 
    { 
        get => (SortDirection)(ViewState["SortDirection"] ?? SortDirection.Descending); 
        set => ViewState["SortDirection"] = value; 
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadOrdersAsync();
        }
    }
    
    private async Task LoadOrdersAsync()
    {
        try
        {
            var orderRequest = new OrderListRequest
            {
                PageIndex = CurrentPage,
                PageSize = GridView1.PageSize,
                SortExpression = this.SortExpression,
                SortDirection = this.SortDirection
            };
            
            var pagedOrders = await _orderService.GetOrdersAsync(orderRequest);
            
            GridView1.DataSource = pagedOrders.Items;
            GridView1.VirtualItemCount = pagedOrders.TotalCount;
            GridView1.DataBind();
        }
        catch (Exception ex)
        {
            ShowErrorMessage("Failed to load orders");
        }
    }
    
    protected async void GridView_PageIndexChanging(object sender, GridViewPageEventArgs e)
    {
        CurrentPage = e.NewPageIndex;
        await LoadOrdersAsync();
    }
    
    protected async void GridView_Sorting(object sender, GridViewSortEventArgs e)
    {
        if (SortExpression == e.SortExpression)
        {
            SortDirection = SortDirection == SortDirection.Ascending ? SortDirection.Descending : SortDirection.Ascending;
        }
        else
        {
            SortExpression = e.SortExpression;
            SortDirection = SortDirection.Ascending;
        }
        
        CurrentPage = 0; // Reset to first page when sorting
        await LoadOrdersAsync();
    }
}

// Service Layer with Paging Support
public class OrderService : IOrderService
{
    private readonly IOrderRepository _repository;
    
    public async Task<PagedResult<Order>> GetOrdersAsync(OrderListRequest request)
    {
        var totalCount = await _repository.GetOrderCountAsync(request.Filter);
        
        var orders = await _repository.GetOrdersAsync(
            request.PageIndex * request.PageSize,
            request.PageSize,
            request.SortExpression,
            request.SortDirection,
            request.Filter
        );
        
        return new PagedResult<Order>
        {
            Items = orders,
            TotalCount = totalCount,
            PageIndex = request.PageIndex,
            PageSize = request.PageSize
        };
    }
}
```

## Event Handling Modernization

### Command Pattern Implementation
```csharp
// Before: Scattered Event Handlers
public partial class UserManagement : Page
{
    protected void btnCreate_Click(object sender, EventArgs e)
    {
        // Validation logic
        if (string.IsNullOrEmpty(txtName.Text))
        {
            lblError.Text = "Name is required";
            return;
        }
        
        // Business logic
        try
        {
            var user = new User
            {
                Name = txtName.Text,
                Email = txtEmail.Text,
                Role = ddlRole.SelectedValue
            };
            
            using (var conn = new SqlConnection(_connectionString))
            {
                var sql = "INSERT INTO Users (Name, Email, Role) VALUES (@Name, @Email, @Role)";
                var cmd = new SqlCommand(sql, conn);
                cmd.Parameters.AddWithValue("@Name", user.Name);
                cmd.Parameters.AddWithValue("@Email", user.Email);
                cmd.Parameters.AddWithValue("@Role", user.Role);
                
                conn.Open();
                cmd.ExecuteNonQuery();
            }
            
            lblSuccess.Text = "User created successfully";
            ClearForm();
            LoadUsers();
        }
        catch (Exception ex)
        {
            lblError.Text = "Failed to create user";
        }
    }
    
    protected void btnUpdate_Click(object sender, EventArgs e)
    {
        // Similar scattered logic...
    }
    
    protected void btnDelete_Click(object sender, EventArgs e)
    {
        // More scattered logic...
    }
}

// After: Command Pattern with Handlers
public abstract class CommandHandler<TRequest, TResponse>
{
    public abstract Task<TResponse> HandleAsync(TRequest request);
}

// Create User Command
public class CreateUserCommand
{
    public string Name { get; set; }
    public string Email { get; set; }
    public string Role { get; set; }
}

public class CreateUserResult
{
    public bool Success { get; set; }
    public string Message { get; set; }
    public int UserId { get; set; }
}

public class CreateUserHandler : CommandHandler<CreateUserCommand, CreateUserResult>
{
    private readonly IUserRepository _repository;
    private readonly IValidator<CreateUserCommand> _validator;
    private readonly ILogger<CreateUserHandler> _logger;
    
    public override async Task<CreateUserResult> HandleAsync(CreateUserCommand request)
    {
        // Validation
        var validationResult = await _validator.ValidateAsync(request);
        if (!validationResult.IsValid)
        {
            return new CreateUserResult
            {
                Success = false,
                Message = string.Join(", ", validationResult.Errors.Select(e => e.ErrorMessage))
            };
        }
        
        // Business logic
        try
        {
            var user = new User
            {
                Name = request.Name,
                Email = request.Email,
                Role = request.Role,
                CreatedDate = DateTime.UtcNow
            };
            
            var userId = await _repository.CreateUserAsync(user);
            
            _logger.LogInformation("User created successfully: {UserId}", userId);
            
            return new CreateUserResult
            {
                Success = true,
                Message = "User created successfully",
                UserId = userId
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to create user");
            return new CreateUserResult
            {
                Success = false,
                Message = "Failed to create user"
            };
        }
    }
}

// Page with Command Handlers
public partial class UserManagement : Page
{
    private readonly CreateUserHandler _createUserHandler;
    private readonly UpdateUserHandler _updateUserHandler;
    private readonly DeleteUserHandler _deleteUserHandler;
    
    protected async void btnCreate_Click(object sender, EventArgs e)
    {
        var command = new CreateUserCommand
        {
            Name = txtName.Text,
            Email = txtEmail.Text,
            Role = ddlRole.SelectedValue
        };
        
        var result = await _createUserHandler.HandleAsync(command);
        
        if (result.Success)
        {
            ShowSuccessMessage(result.Message);
            ClearForm();
            await LoadUsersAsync();
        }
        else
        {
            ShowErrorMessage(result.Message);
        }
    }
}
```

## Dependency Injection Integration

### WebForms DI Container Setup
```csharp
// Global.asax.cs
public class Global : HttpApplication
{
    protected void Application_Start(object sender, EventArgs e)
    {
        // Configure dependency injection
        var services = new ServiceCollection();
        ConfigureServices(services);
        
        var serviceProvider = services.BuildServiceProvider();
        
        // Register custom page handler factory
        PageHandlerFactory.ServiceProvider = serviceProvider;
    }
    
    private void ConfigureServices(IServiceCollection services)
    {
        // Data access
        services.AddScoped<IUserRepository, UserRepository>();
        services.AddScoped<IProductRepository, ProductRepository>();
        
        // Business services
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IProductService, ProductService>();
        
        // Command handlers
        services.AddScoped<CreateUserHandler>();
        services.AddScoped<UpdateUserHandler>();
        services.AddScoped<DeleteUserHandler>();
        
        // Validators
        services.AddScoped<IValidator<CreateUserCommand>, CreateUserValidator>();
        
        // Configuration
        services.AddSingleton<IConfiguration>(provider =>
        {
            return new ConfigurationBuilder()
                .AddAppSettings()
                .Build();
        });
        
        // Logging
        services.AddLogging(builder =>
        {
            builder.AddConsole();
            builder.AddEventLog();
        });
    }
}

// Custom Page Handler Factory
public class PageHandlerFactory : IHttpHandlerFactory
{
    public static IServiceProvider ServiceProvider { get; set; }
    
    public IHttpHandler GetHandler(HttpContext context, string requestType, string url, string pathTranslated)
    {
        var page = (Page)Activator.CreateInstance(GetPageType(pathTranslated));
        
        // Inject dependencies
        InjectDependencies(page);
        
        return page;
    }
    
    private void InjectDependencies(Page page)
    {
        var pageType = page.GetType();
        var constructors = pageType.GetConstructors();
        
        foreach (var constructor in constructors)
        {
            var parameters = constructor.GetParameters();
            if (parameters.Length > 0)
            {
                var args = parameters.Select(p => ServiceProvider.GetService(p.ParameterType)).ToArray();
                constructor.Invoke(page, args);
                break;
            }
        }
    }
}

// Page with Dependency Injection
public partial class ProductList : Page
{
    private readonly IProductService _productService;
    private readonly ICategoryService _categoryService;
    private readonly ILogger<ProductList> _logger;
    
    public ProductList() { } // Parameterless constructor required by WebForms
    
    public ProductList(
        IProductService productService, 
        ICategoryService categoryService,
        ILogger<ProductList> logger)
    {
        _productService = productService;
        _categoryService = categoryService;
        _logger = logger;
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (_productService == null)
        {
            _logger?.LogError("ProductService not injected properly");
            ShowErrorMessage("Application configuration error");
            return;
        }
        
        if (!IsPostBack)
        {
            await LoadDataAsync();
        }
    }
}
```

## Async/Await Pattern Implementation

### Asynchronous Page Operations
```csharp
// Before: Synchronous blocking operations
public partial class DataIntensivePage : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadCategories();
            LoadProducts();
            LoadCustomers();
            LoadOrders();
        }
    }
    
    private void LoadCategories()
    {
        // Blocking database call
        using (var conn = new SqlConnection(_connectionString))
        {
            conn.Open();
            var cmd = new SqlCommand("SELECT * FROM Categories", conn);
            var reader = cmd.ExecuteReader();
            
            var categories = new List<Category>();
            while (reader.Read())
            {
                categories.Add(new Category 
                { 
                    Id = (int)reader["Id"], 
                    Name = reader["Name"].ToString() 
                });
            }
            
            ddlCategory.DataSource = categories;
            ddlCategory.DataBind();
        }
    }
}

// After: Asynchronous non-blocking operations
public partial class DataIntensivePage : Page
{
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadDataAsync();
        }
    }
    
    private async Task LoadDataAsync()
    {
        try
        {
            // Load data in parallel for better performance
            var loadTasks = new[]
            {
                LoadCategoriesAsync(),
                LoadProductsAsync(),
                LoadCustomersAsync(),
                LoadOrdersAsync()
            };
            
            await Task.WhenAll(loadTasks);
            
            lblLoadingStatus.Text = "Data loaded successfully";
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load page data");
            ShowErrorMessage("Failed to load data");
        }
    }
    
    private async Task LoadCategoriesAsync()
    {
        var categories = await _categoryService.GetCategoriesAsync();
        
        ddlCategory.DataSource = categories;
        ddlCategory.DataBind();
    }
    
    private async Task LoadProductsAsync()
    {
        var products = await _productService.GetProductsAsync();
        
        GridView1.DataSource = products;
        GridView1.DataBind();
    }
    
    protected async void btnRefresh_Click(object sender, EventArgs e)
    {
        btnRefresh.Enabled = false;
        lblLoadingStatus.Text = "Refreshing data...";
        
        try
        {
            await LoadDataAsync();
        }
        finally
        {
            btnRefresh.Enabled = true;
        }
    }
}

// Service layer with async methods
public class CategoryService : ICategoryService
{
    private readonly ICategoryRepository _repository;
    
    public async Task<List<Category>> GetCategoriesAsync()
    {
        return await _repository.GetCategoriesAsync();
    }
}

public class CategoryRepository : ICategoryRepository
{
    private readonly string _connectionString;
    
    public async Task<List<Category>> GetCategoriesAsync()
    {
        using var connection = new SqlConnection(_connectionString);
        var sql = "SELECT Id, Name, Description FROM Categories ORDER BY Name";
        
        var categories = await connection.QueryAsync<Category>(sql);
        return categories.ToList();
    }
}
```

## Error Handling and Logging Patterns

### Centralized Error Handling
```csharp
// Base Page with Error Handling
public class BasePage : Page
{
    protected ILogger Logger { get; private set; }
    
    protected override void OnInit(EventArgs e)
    {
        base.OnInit(e);
        Logger = DependencyResolver.Current.GetService<ILogger<BasePage>>();
    }
    
    protected void ShowErrorMessage(string message, Exception ex = null)
    {
        if (ex != null)
        {
            Logger?.LogError(ex, "Page error: {Message}", message);
        }
        
        var errorPanel = FindControl("errorPanel") as Panel;
        var errorLabel = FindControl("lblError") as Label;
        
        if (errorPanel != null && errorLabel != null)
        {
            errorLabel.Text = message;
            errorPanel.Visible = true;
        }
    }
    
    protected void ShowSuccessMessage(string message)
    {
        var successPanel = FindControl("successPanel") as Panel;
        var successLabel = FindControl("lblSuccess") as Label;
        
        if (successPanel != null && successLabel != null)
        {
            successLabel.Text = message;
            successPanel.Visible = true;
        }
    }
    
    protected override void OnError(EventArgs e)
    {
        var exception = Server.GetLastError();
        Logger?.LogError(exception, "Unhandled page error on {PagePath}", Request.Path);
        
        // Clear the error
        Server.ClearError();
        
        // Redirect to error page or show friendly message
        ShowErrorMessage("An unexpected error occurred. Please try again.");
        
        base.OnError(e);
    }
}

// Application-level Error Handling
public class Global : HttpApplication
{
    protected void Application_Error(object sender, EventArgs e)
    {
        var exception = Server.GetLastError();
        var logger = DependencyResolver.Current.GetService<ILogger<Global>>();
        
        logger?.LogError(exception, "Unhandled application error");
        
        // Log additional context
        var context = HttpContext.Current;
        if (context != null)
        {
            logger?.LogError("Error Context - URL: {Url}, User: {User}, SessionId: {SessionId}",
                context.Request.Url?.ToString(),
                context.User?.Identity?.Name ?? "Anonymous",
                context.Session?.SessionID ?? "No Session");
        }
        
        Server.ClearError();
        
        // Redirect based on error type
        if (exception is HttpException httpEx)
        {
            switch (httpEx.GetHttpCode())
            {
                case 404:
                    Response.Redirect("~/Errors/NotFound.aspx");
                    break;
                case 500:
                    Response.Redirect("~/Errors/ServerError.aspx");
                    break;
                default:
                    Response.Redirect("~/Errors/GeneralError.aspx");
                    break;
            }
        }
        else
        {
            Response.Redirect("~/Errors/GeneralError.aspx");
        }
    }
}
```

## Performance Optimization Patterns

### Lazy Loading and Caching
```csharp
// Lazy Loading Pattern
public partial class ProductCatalog : BasePage
{
    private readonly Lazy<IProductService> _productService;
    private readonly Lazy<ICacheService> _cacheService;
    
    public ProductCatalog()
    {
        _productService = new Lazy<IProductService>(() => 
            DependencyResolver.Current.GetService<IProductService>());
        _cacheService = new Lazy<ICacheService>(() => 
            DependencyResolver.Current.GetService<ICacheService>());
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadProductsWithCachingAsync();
        }
    }
    
    private async Task LoadProductsWithCachingAsync()
    {
        const string cacheKey = "ProductCatalog_AllProducts";
        
        try
        {
            // Try to get from cache first
            var cachedProducts = await _cacheService.Value.GetAsync<List<Product>>(cacheKey);
            
            if (cachedProducts != null)
            {
                BindProducts(cachedProducts);
                lblCacheStatus.Text = "Data loaded from cache";
                return;
            }
            
            // Load from database
            var products = await _productService.Value.GetProductsAsync();
            
            // Cache for 15 minutes
            await _cacheService.Value.SetAsync(cacheKey, products, TimeSpan.FromMinutes(15));
            
            BindProducts(products);
            lblCacheStatus.Text = "Data loaded from database";
        }
        catch (Exception ex)
        {
            ShowErrorMessage("Failed to load products", ex);
        }
    }
    
    private void BindProducts(List<Product> products)
    {
        // Implement virtual paging for large datasets
        var pageSize = 20;
        var pageIndex = GetCurrentPageIndex();
        
        var pagedProducts = products
            .Skip(pageIndex * pageSize)
            .Take(pageSize)
            .ToList();
        
        Repeater1.DataSource = pagedProducts;
        Repeater1.DataBind();
        
        // Update paging controls
        UpdatePagingControls(products.Count, pageSize, pageIndex);
    }
}

// Caching Service Implementation
public class CacheService : ICacheService
{
    private readonly IMemoryCache _memoryCache;
    private readonly IDistributedCache _distributedCache;
    
    public async Task<T> GetAsync<T>(string key) where T : class
    {
        // Try memory cache first (fastest)
        if (_memoryCache.TryGetValue(key, out T memoryValue))
        {
            return memoryValue;
        }
        
        // Try distributed cache (slower but shared)
        var distributedData = await _distributedCache.GetStringAsync(key);
        if (distributedData != null)
        {
            var distributedValue = JsonSerializer.Deserialize<T>(distributedData);
            
            // Store in memory cache for faster subsequent access
            _memoryCache.Set(key, distributedValue, TimeSpan.FromMinutes(5));
            
            return distributedValue;
        }
        
        return null;
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan expiration) where T : class
    {
        // Store in memory cache
        _memoryCache.Set(key, value, expiration);
        
        // Store in distributed cache
        var serializedValue = JsonSerializer.Serialize(value);
        var distributedOptions = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = expiration
        };
        
        await _distributedCache.SetStringAsync(key, serializedValue, distributedOptions);
    }
}
```

## Custom Control Refactoring

### Convert Server Controls to Components
```csharp
// Before: Custom Server Control
[ToolboxData("<{0}:PagingControl runat=server></{0}:PagingControl>")]
public class PagingControl : CompositeControl
{
    public int TotalRecords { get; set; }
    public int PageSize { get; set; } = 10;
    public int CurrentPage { get; set; } = 0;
    
    public event EventHandler<PageChangedEventArgs> PageChanged;
    
    protected override void CreateChildControls()
    {
        Controls.Clear();
        
        var totalPages = (int)Math.Ceiling((double)TotalRecords / PageSize);
        
        // Previous button
        if (CurrentPage > 0)
        {
            var prevButton = new LinkButton
            {
                Text = "« Previous",
                CommandArgument = (CurrentPage - 1).ToString(),
                CssClass = "paging-link"
            };
            prevButton.Click += PageButton_Click;
            Controls.Add(prevButton);
        }
        
        // Page numbers
        for (int i = 0; i < totalPages; i++)
        {
            var pageButton = new LinkButton
            {
                Text = (i + 1).ToString(),
                CommandArgument = i.ToString(),
                CssClass = i == CurrentPage ? "paging-link active" : "paging-link"
            };
            pageButton.Click += PageButton_Click;
            Controls.Add(pageButton);
        }
        
        // Next button
        if (CurrentPage < totalPages - 1)
        {
            var nextButton = new LinkButton
            {
                Text = "Next »",
                CommandArgument = (CurrentPage + 1).ToString(),
                CssClass = "paging-link"
            };
            nextButton.Click += PageButton_Click;
            Controls.Add(nextButton);
        }
    }
    
    private void PageButton_Click(object sender, EventArgs e)
    {
        var button = (LinkButton)sender;
        var newPage = Convert.ToInt32(button.CommandArgument);
        
        CurrentPage = newPage;
        
        PageChanged?.Invoke(this, new PageChangedEventArgs { NewPageIndex = newPage });
    }
}

// After: Modern User Control Component
public partial class PagingComponent : UserControl
{
    public event EventHandler<PageChangedEventArgs> PageChanged;
    
    public int TotalRecords
    {
        get => ViewState["TotalRecords"] as int? ?? 0;
        set => ViewState["TotalRecords"] = value;
    }
    
    public int PageSize
    {
        get => ViewState["PageSize"] as int? ?? 10;
        set => ViewState["PageSize"] = value;
    }
    
    public int CurrentPage
    {
        get => ViewState["CurrentPage"] as int? ?? 0;
        set => ViewState["CurrentPage"] = value;
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            BuildPagingInterface();
        }
    }
    
    private void BuildPagingInterface()
    {
        var totalPages = (int)Math.Ceiling((double)TotalRecords / PageSize);
        
        // Use Repeater for cleaner markup
        rptPaging.DataSource = GeneratePagingData(totalPages);
        rptPaging.DataBind();
        
        // Show/hide navigation buttons
        btnPrevious.Visible = CurrentPage > 0;
        btnNext.Visible = CurrentPage < totalPages - 1;
        
        if (btnPrevious.Visible)
            btnPrevious.CommandArgument = (CurrentPage - 1).ToString();
        
        if (btnNext.Visible)
            btnNext.CommandArgument = (CurrentPage + 1).ToString();
    }
    
    private List<PagingItem> GeneratePagingData(int totalPages)
    {
        var items = new List<PagingItem>();
        
        // Smart paging - show ellipsis for large page counts
        var startPage = Math.Max(0, CurrentPage - 5);
        var endPage = Math.Min(totalPages - 1, CurrentPage + 5);
        
        for (int i = startPage; i <= endPage; i++)
        {
            items.Add(new PagingItem
            {
                PageNumber = i + 1,
                PageIndex = i,
                IsActive = i == CurrentPage,
                IsEllipsis = false
            });
        }
        
        return items;
    }
    
    protected void NavigationButton_Click(object sender, EventArgs e)
    {
        var button = (Button)sender;
        var newPage = Convert.ToInt32(button.CommandArgument);
        
        CurrentPage = newPage;
        BuildPagingInterface();
        
        PageChanged?.Invoke(this, new PageChangedEventArgs { NewPageIndex = newPage });
    }
    
    protected void rptPaging_ItemCommand(object source, RepeaterCommandEventArgs e)
    {
        if (e.CommandName == "Page")
        {
            var newPage = Convert.ToInt32(e.CommandArgument);
            CurrentPage = newPage;
            BuildPagingInterface();
            
            PageChanged?.Invoke(this, new PageChangedEventArgs { NewPageIndex = newPage });
        }
    }
}

// Supporting classes
public class PagingItem
{
    public int PageNumber { get; set; }
    public int PageIndex { get; set; }
    public bool IsActive { get; set; }
    public bool IsEllipsis { get; set; }
}

public class PageChangedEventArgs : EventArgs
{
    public int NewPageIndex { get; set; }
}
```

## Testing Support Refactoring

### Testable WebForms Architecture
```csharp
// Abstract base for testable pages
public abstract class TestableBasePage : Page
{
    protected abstract void InitializeServices();
    protected abstract Task LoadPageDataAsync();
    
    protected sealed override async void OnLoad(EventArgs e)
    {
        InitializeServices();
        
        if (!IsPostBack)
        {
            await LoadPageDataAsync();
        }
        
        base.OnLoad(e);
    }
}

// Testable page implementation
public partial class ProductList : TestableBasePage
{
    private IProductService _productService;
    private ICategoryService _categoryService;
    
    // For testing - allow service injection
    public void InjectServices(IProductService productService, ICategoryService categoryService)
    {
        _productService = productService;
        _categoryService = categoryService;
    }
    
    protected override void InitializeServices()
    {
        if (_productService == null) // Not injected for testing
        {
            _productService = DependencyResolver.Current.GetService<IProductService>();
            _categoryService = DependencyResolver.Current.GetService<ICategoryService>();
        }
    }
    
    protected override async Task LoadPageDataAsync()
    {
        await LoadCategoriesAsync();
        await LoadProductsAsync();
    }
    
    // Make methods public/internal for testing
    internal async Task LoadCategoriesAsync()
    {
        var categories = await _categoryService.GetCategoriesAsync();
        ddlCategory.DataSource = categories;
        ddlCategory.DataBind();
    }
    
    internal async Task LoadProductsAsync()
    {
        var categoryId = Convert.ToInt32(ddlCategory.SelectedValue);
        var products = categoryId == 0 
            ? await _productService.GetProductsAsync()
            : await _productService.GetProductsByCategoryAsync(categoryId);
            
        GridView1.DataSource = products;
        GridView1.DataBind();
    }
}

// Unit tests
[TestClass]
public class ProductListTests
{
    private Mock<IProductService> _mockProductService;
    private Mock<ICategoryService> _mockCategoryService;
    private ProductList _page;
    
    [TestInitialize]
    public void Setup()
    {
        _mockProductService = new Mock<IProductService>();
        _mockCategoryService = new Mock<ICategoryService>();
        _page = new ProductList();
        
        // Inject mocked services
        _page.InjectServices(_mockProductService.Object, _mockCategoryService.Object);
    }
    
    [TestMethod]
    public async Task LoadCategoriesAsync_ShouldBindCategoriesToDropdown()
    {
        // Arrange
        var categories = new List<Category>
        {
            new Category { Id = 1, Name = "Category 1" },
            new Category { Id = 2, Name = "Category 2" }
        };
        
        _mockCategoryService.Setup(x => x.GetCategoriesAsync())
                          .ReturnsAsync(categories);
        
        // Act
        await _page.LoadCategoriesAsync();
        
        // Assert
        _mockCategoryService.Verify(x => x.GetCategoriesAsync(), Times.Once);
        Assert.AreEqual(2, _page.ddlCategory.Items.Count);
    }
}
```

## Configuration and Settings Modernization

### Configuration Management
```csharp
// Before: Direct configuration access
public partial class DatabasePage : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        var connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;
        var timeout = Convert.ToInt32(ConfigurationManager.AppSettings["CommandTimeout"]);
        var enableCaching = Convert.ToBoolean(ConfigurationManager.AppSettings["EnableCaching"]);
        
        // Use configuration values directly
        LoadData(connectionString, timeout, enableCaching);
    }
}

// After: Strongly-typed configuration
public class DatabaseSettings
{
    public string ConnectionString { get; set; }
    public int CommandTimeout { get; set; } = 30;
    public bool EnableCaching { get; set; } = true;
}

public interface IApplicationSettings
{
    DatabaseSettings Database { get; }
    CachingSettings Caching { get; }
    LoggingSettings Logging { get; }
}

public class ApplicationSettings : IApplicationSettings
{
    public DatabaseSettings Database { get; private set; }
    public CachingSettings Caching { get; private set; }
    public LoggingSettings Logging { get; private set; }
    
    public ApplicationSettings()
    {
        LoadSettings();
    }
    
    private void LoadSettings()
    {
        Database = new DatabaseSettings
        {
            ConnectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"]?.ConnectionString,
            CommandTimeout = GetAppSetting<int>("Database:CommandTimeout", 30),
            EnableCaching = GetAppSetting<bool>("Database:EnableCaching", true)
        };
        
        Caching = new CachingSettings
        {
            DefaultExpiration = TimeSpan.FromMinutes(GetAppSetting<int>("Caching:DefaultExpirationMinutes", 15)),
            MaxCacheSize = GetAppSetting<long>("Caching:MaxCacheSize", 100 * 1024 * 1024) // 100MB
        };
    }
    
    private T GetAppSetting<T>(string key, T defaultValue)
    {
        var value = ConfigurationManager.AppSettings[key];
        if (string.IsNullOrEmpty(value))
            return defaultValue;
            
        return (T)Convert.ChangeType(value, typeof(T));
    }
}

// Page with injected settings
public partial class DatabasePage : Page
{
    private readonly IApplicationSettings _settings;
    private readonly IDataService _dataService;
    
    public DatabasePage(IApplicationSettings settings, IDataService dataService)
    {
        _settings = settings;
        _dataService = dataService;
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadDataAsync();
        }
    }
    
    private async Task LoadDataAsync()
    {
        var options = new DataLoadOptions
        {
            CommandTimeout = _settings.Database.CommandTimeout,
            EnableCaching = _settings.Database.EnableCaching,
            CacheExpiration = _settings.Caching.DefaultExpiration
        };
        
        var data = await _dataService.LoadDataAsync(options);
        BindData(data);
    }
}
```

## Conclusion

These refactoring patterns provide a systematic approach to modernizing WebForms applications while maintaining functionality. The key principles are:

1. **Separation of Concerns**: Extract business logic from code-behind
2. **Dependency Injection**: Enable testability and maintainability
3. **Async/Await**: Improve performance and scalability
4. **Error Handling**: Centralize and standardize error management
5. **Configuration**: Use strongly-typed configuration classes
6. **Testing**: Make code testable through proper abstraction

By applying these patterns incrementally, teams can modernize WebForms applications step by step, reducing technical debt while preparing for eventual migration to modern frameworks.