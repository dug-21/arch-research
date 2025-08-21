# WebForms Code Patterns Catalog

## Table of Contents
1. [Page Patterns](#page-patterns)
2. [Control Patterns](#control-patterns)
3. [Data Access Patterns](#data-access-patterns)
4. [State Management Patterns](#state-management-patterns)
5. [Event Handling Patterns](#event-handling-patterns)
6. [Security Patterns](#security-patterns)
7. [Performance Patterns](#performance-patterns)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Page Patterns

### 1. Base Page Pattern

**Purpose**: Centralize common functionality across multiple pages.

```csharp
// BasePage.cs - Common base class
public class BasePage : System.Web.UI.Page
{
    protected override void OnInit(EventArgs e)
    {
        base.OnInit(e);
        
        // Common initialization
        SetupSecurity();
        InitializeLogging();
        ConfigureTheme();
    }
    
    protected override void OnLoad(EventArgs e)
    {
        base.OnLoad(e);
        
        // Common loading logic
        if (!IsPostBack)
        {
            LoadUserPreferences();
            SetupNavigationContext();
        }
    }
    
    protected virtual void SetupSecurity()
    {
        if (!User.Identity.IsAuthenticated && RequiresAuthentication)
        {
            Response.Redirect("~/Login.aspx");
        }
    }
    
    protected virtual bool RequiresAuthentication => true;
    
    protected void LogPageView()
    {
        // Centralized logging
        Logger.Info($"Page viewed: {Request.Url.AbsolutePath} by {User.Identity.Name}");
    }
    
    protected void ShowMessage(string message, MessageType type)
    {
        // Common message display mechanism
        var messageControl = Master.FindControl("MessagePanel") as Panel;
        if (messageControl != null)
        {
            var label = new Label
            {
                Text = message,
                CssClass = $"message-{type.ToString().ToLower()}"
            };
            messageControl.Controls.Add(label);
        }
    }
}

// Usage in derived pages
public partial class ProductList : BasePage
{
    protected override bool RequiresAuthentication => false; // Public page
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
            LogPageView();
        }
    }
}
```

### 2. Page Controller Pattern

**Purpose**: Separate page logic from UI concerns.

```csharp
// ProductController.cs - Business logic
public class ProductController
{
    private readonly IProductService _productService;
    
    public ProductController(IProductService productService)
    {
        _productService = productService;
    }
    
    public PageResult<Product> GetProducts(int pageIndex, int pageSize, string searchTerm = null)
    {
        try
        {
            var products = _productService.GetProducts(pageIndex, pageSize, searchTerm);
            return new PageResult<Product>
            {
                Data = products.Items,
                TotalCount = products.TotalCount,
                Success = true
            };
        }
        catch (Exception ex)
        {
            return new PageResult<Product>
            {
                Success = false,
                ErrorMessage = "Failed to load products: " + ex.Message
            };
        }
    }
    
    public OperationResult AddProduct(Product product)
    {
        try
        {
            _productService.AddProduct(product);
            return new OperationResult { Success = true };
        }
        catch (ValidationException ex)
        {
            return new OperationResult
            {
                Success = false,
                ErrorMessage = ex.Message
            };
        }
    }
}

// ProductList.aspx.cs - UI layer
public partial class ProductList : BasePage
{
    private readonly ProductController _controller;
    
    public ProductList()
    {
        _controller = new ProductController(new ProductService());
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    private void LoadProducts()
    {
        var result = _controller.GetProducts(0, 20, txtSearch.Text);
        
        if (result.Success)
        {
            gvProducts.DataSource = result.Data;
            gvProducts.DataBind();
        }
        else
        {
            ShowMessage(result.ErrorMessage, MessageType.Error);
        }
    }
    
    protected void btnSearch_Click(object sender, EventArgs e)
    {
        LoadProducts();
    }
}
```

### 3. MVP (Model-View-Presenter) Pattern

**Purpose**: Achieve better testability and separation of concerns.

```csharp
// IProductView.cs - View interface
public interface IProductView
{
    string SearchTerm { get; }
    void DisplayProducts(IEnumerable<Product> products);
    void DisplayError(string message);
    void DisplaySuccess(string message);
    event EventHandler SearchClicked;
    event EventHandler<ProductEventArgs> ProductSelected;
}

// ProductPresenter.cs - Presenter
public class ProductPresenter
{
    private readonly IProductView _view;
    private readonly IProductService _productService;
    
    public ProductPresenter(IProductView view, IProductService productService)
    {
        _view = view;
        _productService = productService;
        
        _view.SearchClicked += OnSearchClicked;
        _view.ProductSelected += OnProductSelected;
    }
    
    public void Initialize()
    {
        LoadProducts();
    }
    
    private void OnSearchClicked(object sender, EventArgs e)
    {
        LoadProducts();
    }
    
    private void OnProductSelected(object sender, ProductEventArgs e)
    {
        // Handle product selection
        var product = _productService.GetProduct(e.ProductId);
        // Navigate to product details
    }
    
    private void LoadProducts()
    {
        try
        {
            var products = _productService.SearchProducts(_view.SearchTerm);
            _view.DisplayProducts(products);
        }
        catch (Exception ex)
        {
            _view.DisplayError($"Failed to load products: {ex.Message}");
        }
    }
}

// ProductList.aspx.cs - View implementation
public partial class ProductList : BasePage, IProductView
{
    private ProductPresenter _presenter;
    
    public string SearchTerm => txtSearch.Text;
    
    public event EventHandler SearchClicked;
    public event EventHandler<ProductEventArgs> ProductSelected;
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (_presenter == null)
        {
            _presenter = new ProductPresenter(this, new ProductService());
        }
        
        if (!IsPostBack)
        {
            _presenter.Initialize();
        }
    }
    
    public void DisplayProducts(IEnumerable<Product> products)
    {
        gvProducts.DataSource = products;
        gvProducts.DataBind();
    }
    
    public void DisplayError(string message)
    {
        ShowMessage(message, MessageType.Error);
    }
    
    public void DisplaySuccess(string message)
    {
        ShowMessage(message, MessageType.Success);
    }
    
    protected void btnSearch_Click(object sender, EventArgs e)
    {
        SearchClicked?.Invoke(sender, e);
    }
    
    protected void gvProducts_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        if (e.CommandName == "Select")
        {
            var productId = Convert.ToInt32(e.CommandArgument);
            ProductSelected?.Invoke(this, new ProductEventArgs(productId));
        }
    }
}
```

## Control Patterns

### 1. Composite Control Pattern

**Purpose**: Create reusable complex controls.

```csharp
// AddressControl.ascx - User control
public partial class AddressControl : UserControl
{
    public string Street
    {
        get { return txtStreet.Text; }
        set { txtStreet.Text = value; }
    }
    
    public string City
    {
        get { return txtCity.Text; }
        set { txtCity.Text = value; }
    }
    
    public string State
    {
        get { return ddlState.SelectedValue; }
        set { ddlState.SelectedValue = value; }
    }
    
    public string ZipCode
    {
        get { return txtZipCode.Text; }
        set { txtZipCode.Text = value; }
    }
    
    public Address Address
    {
        get
        {
            return new Address
            {
                Street = Street,
                City = City,
                State = State,
                ZipCode = ZipCode
            };
        }
        set
        {
            if (value != null)
            {
                Street = value.Street;
                City = value.City;
                State = value.State;
                ZipCode = value.ZipCode;
            }
        }
    }
    
    public bool IsValid()
    {
        var isValid = true;
        
        if (string.IsNullOrWhiteSpace(Street))
        {
            lblStreetError.Text = "Street is required";
            lblStreetError.Visible = true;
            isValid = false;
        }
        
        if (string.IsNullOrWhiteSpace(City))
        {
            lblCityError.Text = "City is required";
            lblCityError.Visible = true;
            isValid = false;
        }
        
        return isValid;
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadStates();
        }
    }
    
    private void LoadStates()
    {
        ddlState.DataSource = StateProvider.GetStates();
        ddlState.DataTextField = "Name";
        ddlState.DataValueField = "Code";
        ddlState.DataBind();
        ddlState.Items.Insert(0, new ListItem("Select State", ""));
    }
}

// Usage in parent page
public partial class CustomerEdit : BasePage
{
    protected void btnSave_Click(object sender, EventArgs e)
    {
        if (addressControl.IsValid())
        {
            var customer = new Customer
            {
                Name = txtName.Text,
                Address = addressControl.Address
            };
            
            SaveCustomer(customer);
        }
    }
}
```

### 2. Custom Server Control Pattern

**Purpose**: Create highly reusable, feature-rich controls.

```csharp
// PagingGridView.cs - Custom server control
[ToolboxData("<{0}:PagingGridView runat=server></{0}:PagingGridView>")]
public class PagingGridView : CompositeControl
{
    private GridView _gridView;
    private Label _infoLabel;
    private Button _prevButton;
    private Button _nextButton;
    
    public int PageSize
    {
        get { return ViewState["PageSize"] != null ? (int)ViewState["PageSize"] : 10; }
        set { ViewState["PageSize"] = value; }
    }
    
    public int CurrentPage
    {
        get { return ViewState["CurrentPage"] != null ? (int)ViewState["CurrentPage"] : 0; }
        set { ViewState["CurrentPage"] = value; }
    }
    
    public object DataSource
    {
        get { return _gridView?.DataSource; }
        set 
        { 
            EnsureChildControls();
            _gridView.DataSource = value;
        }
    }
    
    public event EventHandler<PageChangedEventArgs> PageChanged;
    
    protected override void CreateChildControls()
    {
        Controls.Clear();
        
        // Create grid view
        _gridView = new GridView
        {
            ID = "GridView1",
            AutoGenerateColumns = false,
            CssClass = "data-grid"
        };
        
        // Create paging controls
        var pagingPanel = new Panel { CssClass = "paging-panel" };
        
        _prevButton = new Button
        {
            ID = "btnPrev",
            Text = "Previous",
            CssClass = "paging-button"
        };
        _prevButton.Click += PrevButton_Click;
        
        _infoLabel = new Label
        {
            ID = "lblInfo",
            CssClass = "paging-info"
        };
        
        _nextButton = new Button
        {
            ID = "btnNext",
            Text = "Next",
            CssClass = "paging-button"
        };
        _nextButton.Click += NextButton_Click;
        
        pagingPanel.Controls.Add(_prevButton);
        pagingPanel.Controls.Add(new LiteralControl(" "));
        pagingPanel.Controls.Add(_infoLabel);
        pagingPanel.Controls.Add(new LiteralControl(" "));
        pagingPanel.Controls.Add(_nextButton);
        
        Controls.Add(_gridView);
        Controls.Add(pagingPanel);
    }
    
    public override void DataBind()
    {
        EnsureChildControls();
        
        if (DataSource is IEnumerable<object> data)
        {
            var pagedData = data.Skip(CurrentPage * PageSize).Take(PageSize);
            _gridView.DataSource = pagedData;
            _gridView.DataBind();
            
            UpdatePagingInfo(data.Count());
        }
    }
    
    private void UpdatePagingInfo(int totalRecords)
    {
        var totalPages = (int)Math.Ceiling((double)totalRecords / PageSize);
        var startRecord = CurrentPage * PageSize + 1;
        var endRecord = Math.Min((CurrentPage + 1) * PageSize, totalRecords);
        
        _infoLabel.Text = $"Showing {startRecord}-{endRecord} of {totalRecords}";
        _prevButton.Enabled = CurrentPage > 0;
        _nextButton.Enabled = CurrentPage < totalPages - 1;
    }
    
    private void PrevButton_Click(object sender, EventArgs e)
    {
        if (CurrentPage > 0)
        {
            CurrentPage--;
            OnPageChanged();
        }
    }
    
    private void NextButton_Click(object sender, EventArgs e)
    {
        CurrentPage++;
        OnPageChanged();
    }
    
    protected virtual void OnPageChanged()
    {
        PageChanged?.Invoke(this, new PageChangedEventArgs(CurrentPage));
    }
}

// Usage
public partial class ProductList : BasePage
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    protected void pagingGrid_PageChanged(object sender, PageChangedEventArgs e)
    {
        LoadProducts();
    }
    
    private void LoadProducts()
    {
        var products = GetProducts();
        pagingGrid.DataSource = products;
        pagingGrid.DataBind();
    }
}
```

## Data Access Patterns

### 1. Repository Pattern

**Purpose**: Abstract data access logic and improve testability.

```csharp
// IRepository.cs - Generic repository interface
public interface IRepository<T> where T : class
{
    T GetById(int id);
    IEnumerable<T> GetAll();
    IEnumerable<T> Find(Expression<Func<T, bool>> predicate);
    void Add(T entity);
    void Update(T entity);
    void Delete(T entity);
    void Delete(int id);
}

// ProductRepository.cs - Concrete implementation
public class ProductRepository : IRepository<Product>
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
                        return MapProduct(reader);
                    }
                }
            }
        }
        return null;
    }
    
    public IEnumerable<Product> GetAll()
    {
        var products = new List<Product>();
        
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            using (var command = new SqlCommand("SELECT * FROM Products", connection))
            {
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        products.Add(MapProduct(reader));
                    }
                }
            }
        }
        
        return products;
    }
    
    public void Add(Product product)
    {
        using (var connection = new SqlConnection(_connectionString))
        {
            connection.Open();
            using (var command = new SqlCommand(
                "INSERT INTO Products (Name, Price, Description) VALUES (@Name, @Price, @Description)", 
                connection))
            {
                command.Parameters.AddWithValue("@Name", product.Name);
                command.Parameters.AddWithValue("@Price", product.Price);
                command.Parameters.AddWithValue("@Description", product.Description ?? (object)DBNull.Value);
                command.ExecuteNonQuery();
            }
        }
    }
    
    private Product MapProduct(SqlDataReader reader)
    {
        return new Product
        {
            Id = reader.GetInt32("Id"),
            Name = reader.GetString("Name"),
            Price = reader.GetDecimal("Price"),
            Description = reader.IsDBNull("Description") ? null : reader.GetString("Description")
        };
    }
}

// Usage in page
public partial class ProductManagement : BasePage
{
    private readonly IRepository<Product> _productRepository;
    
    public ProductManagement()
    {
        _productRepository = new ProductRepository(ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString);
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    private void LoadProducts()
    {
        var products = _productRepository.GetAll();
        gvProducts.DataSource = products;
        gvProducts.DataBind();
    }
    
    protected void btnAdd_Click(object sender, EventArgs e)
    {
        var product = new Product
        {
            Name = txtName.Text,
            Price = decimal.Parse(txtPrice.Text),
            Description = txtDescription.Text
        };
        
        _productRepository.Add(product);
        LoadProducts();
        ClearForm();
    }
}
```

### 2. Data Access Layer (DAL) Pattern

**Purpose**: Centralize and standardize data access operations.

```csharp
// DataAccessBase.cs - Base DAL class
public abstract class DataAccessBase
{
    protected readonly string ConnectionString;
    
    protected DataAccessBase(string connectionString)
    {
        ConnectionString = connectionString;
    }
    
    protected T ExecuteScalar<T>(string sql, params SqlParameter[] parameters)
    {
        using (var connection = new SqlConnection(ConnectionString))
        {
            connection.Open();
            using (var command = new SqlCommand(sql, connection))
            {
                if (parameters != null)
                {
                    command.Parameters.AddRange(parameters);
                }
                
                var result = command.ExecuteScalar();
                return result == DBNull.Value ? default(T) : (T)result;
            }
        }
    }
    
    protected int ExecuteNonQuery(string sql, params SqlParameter[] parameters)
    {
        using (var connection = new SqlConnection(ConnectionString))
        {
            connection.Open();
            using (var command = new SqlCommand(sql, connection))
            {
                if (parameters != null)
                {
                    command.Parameters.AddRange(parameters);
                }
                
                return command.ExecuteNonQuery();
            }
        }
    }
    
    protected List<T> ExecuteReader<T>(string sql, Func<SqlDataReader, T> mapper, params SqlParameter[] parameters)
    {
        var results = new List<T>();
        
        using (var connection = new SqlConnection(ConnectionString))
        {
            connection.Open();
            using (var command = new SqlCommand(sql, connection))
            {
                if (parameters != null)
                {
                    command.Parameters.AddRange(parameters);
                }
                
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        results.Add(mapper(reader));
                    }
                }
            }
        }
        
        return results;
    }
}

// ProductDAL.cs - Product-specific DAL
public class ProductDAL : DataAccessBase
{
    public ProductDAL(string connectionString) : base(connectionString)
    {
    }
    
    public List<Product> GetProducts()
    {
        return ExecuteReader("SELECT * FROM Products", MapProduct);
    }
    
    public Product GetProduct(int id)
    {
        var products = ExecuteReader(
            "SELECT * FROM Products WHERE Id = @Id",
            MapProduct,
            new SqlParameter("@Id", id));
            
        return products.FirstOrDefault();
    }
    
    public int AddProduct(Product product)
    {
        return ExecuteScalar<int>(
            @"INSERT INTO Products (Name, Price, Description) 
              VALUES (@Name, @Price, @Description);
              SELECT SCOPE_IDENTITY();",
            new SqlParameter("@Name", product.Name),
            new SqlParameter("@Price", product.Price),
            new SqlParameter("@Description", product.Description ?? (object)DBNull.Value));
    }
    
    public void UpdateProduct(Product product)
    {
        ExecuteNonQuery(
            @"UPDATE Products 
              SET Name = @Name, Price = @Price, Description = @Description 
              WHERE Id = @Id",
            new SqlParameter("@Id", product.Id),
            new SqlParameter("@Name", product.Name),
            new SqlParameter("@Price", product.Price),
            new SqlParameter("@Description", product.Description ?? (object)DBNull.Value));
    }
    
    public void DeleteProduct(int id)
    {
        ExecuteNonQuery(
            "DELETE FROM Products WHERE Id = @Id",
            new SqlParameter("@Id", id));
    }
    
    private Product MapProduct(SqlDataReader reader)
    {
        return new Product
        {
            Id = reader.GetInt32("Id"),
            Name = reader.GetString("Name"),
            Price = reader.GetDecimal("Price"),
            Description = reader.IsDBNull("Description") ? null : reader.GetString("Description"),
            CreatedDate = reader.GetDateTime("CreatedDate")
        };
    }
}
```

## State Management Patterns

### 1. Session Wrapper Pattern

**Purpose**: Provide type-safe access to session variables.

```csharp
// SessionHelper.cs - Session wrapper
public static class SessionHelper
{
    private const string USER_ID_KEY = "UserId";
    private const string USER_NAME_KEY = "UserName";
    private const string SHOPPING_CART_KEY = "ShoppingCart";
    private const string USER_PREFERENCES_KEY = "UserPreferences";
    
    public static int? UserId
    {
        get => HttpContext.Current.Session[USER_ID_KEY] as int?;
        set => HttpContext.Current.Session[USER_ID_KEY] = value;
    }
    
    public static string UserName
    {
        get => HttpContext.Current.Session[USER_NAME_KEY] as string;
        set => HttpContext.Current.Session[USER_NAME_KEY] = value;
    }
    
    public static ShoppingCart ShoppingCart
    {
        get
        {
            var cart = HttpContext.Current.Session[SHOPPING_CART_KEY] as ShoppingCart;
            if (cart == null)
            {
                cart = new ShoppingCart();
                HttpContext.Current.Session[SHOPPING_CART_KEY] = cart;
            }
            return cart;
        }
        set => HttpContext.Current.Session[SHOPPING_CART_KEY] = value;
    }
    
    public static UserPreferences UserPreferences
    {
        get
        {
            var prefs = HttpContext.Current.Session[USER_PREFERENCES_KEY] as UserPreferences;
            if (prefs == null)
            {
                prefs = new UserPreferences();
                HttpContext.Current.Session[USER_PREFERENCES_KEY] = prefs;
            }
            return prefs;
        }
        set => HttpContext.Current.Session[USER_PREFERENCES_KEY] = value;
    }
    
    public static void ClearUserSession()
    {
        HttpContext.Current.Session.Remove(USER_ID_KEY);
        HttpContext.Current.Session.Remove(USER_NAME_KEY);
        HttpContext.Current.Session.Remove(SHOPPING_CART_KEY);
        HttpContext.Current.Session.Remove(USER_PREFERENCES_KEY);
    }
    
    public static bool IsUserLoggedIn => UserId.HasValue;
}

// Usage in pages
public partial class ProductDetails : BasePage
{
    protected void btnAddToCart_Click(object sender, EventArgs e)
    {
        if (!SessionHelper.IsUserLoggedIn)
        {
            Response.Redirect("Login.aspx");
            return;
        }
        
        var product = GetProduct();
        SessionHelper.ShoppingCart.AddItem(product);
        
        ShowMessage($"{product.Name} added to cart", MessageType.Success);
    }
}
```

### 2. ViewState Manager Pattern

**Purpose**: Manage complex ViewState scenarios efficiently.

```csharp
// ViewStateManager.cs - ViewState helper
public class ViewStateManager
{
    private readonly Page _page;
    
    public ViewStateManager(Page page)
    {
        _page = page;
    }
    
    public T GetValue<T>(string key, T defaultValue = default(T))
    {
        return _page.ViewState[key] != null ? (T)_page.ViewState[key] : defaultValue;
    }
    
    public void SetValue<T>(string key, T value)
    {
        _page.ViewState[key] = value;
    }
    
    public void RemoveValue(string key)
    {
        _page.ViewState.Remove(key);
    }
    
    public bool HasValue(string key)
    {
        return _page.ViewState[key] != null;
    }
    
    // Strongly-typed properties
    public List<Product> Products
    {
        get => GetValue<List<Product>>("Products") ?? new List<Product>();
        set => SetValue("Products", value);
    }
    
    public int CurrentPage
    {
        get => GetValue("CurrentPage", 0);
        set => SetValue("CurrentPage", value);
    }
    
    public string SortExpression
    {
        get => GetValue<string>("SortExpression");
        set => SetValue("SortExpression", value);
    }
    
    public SortDirection SortDirection
    {
        get => GetValue("SortDirection", SortDirection.Ascending);
        set => SetValue("SortDirection", value);
    }
}

// Usage in page
public partial class ProductList : BasePage
{
    private ViewStateManager _viewState;
    
    protected ViewStateManager ViewStateManager
    {
        get { return _viewState ?? (_viewState = new ViewStateManager(this)); }
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    private void LoadProducts()
    {
        var products = GetProducts(ViewStateManager.SortExpression, ViewStateManager.SortDirection);
        ViewStateManager.Products = products.ToList();
        
        gvProducts.DataSource = ViewStateManager.Products;
        gvProducts.DataBind();
    }
    
    protected void gvProducts_Sorting(object sender, GridViewSortEventArgs e)
    {
        if (ViewStateManager.SortExpression == e.SortExpression)
        {
            ViewStateManager.SortDirection = ViewStateManager.SortDirection == SortDirection.Ascending 
                ? SortDirection.Descending 
                : SortDirection.Ascending;
        }
        else
        {
            ViewStateManager.SortExpression = e.SortExpression;
            ViewStateManager.SortDirection = SortDirection.Ascending;
        }
        
        LoadProducts();
    }
}
```

## Event Handling Patterns

### 1. Command Pattern for Events

**Purpose**: Centralize and standardize event handling logic.

```csharp
// ICommand.cs - Command interface
public interface ICommand
{
    void Execute(object parameter);
    bool CanExecute(object parameter);
}

// ProductCommands.cs - Command implementations
public class AddProductCommand : ICommand
{
    private readonly IProductService _productService;
    
    public AddProductCommand(IProductService productService)
    {
        _productService = productService;
    }
    
    public void Execute(object parameter)
    {
        var product = parameter as Product;
        if (product != null)
        {
            _productService.AddProduct(product);
        }
    }
    
    public bool CanExecute(object parameter)
    {
        var product = parameter as Product;
        return product != null && !string.IsNullOrEmpty(product.Name);
    }
}

public class DeleteProductCommand : ICommand
{
    private readonly IProductService _productService;
    
    public DeleteProductCommand(IProductService productService)
    {
        _productService = productService;
    }
    
    public void Execute(object parameter)
    {
        if (parameter is int productId)
        {
            _productService.DeleteProduct(productId);
        }
    }
    
    public bool CanExecute(object parameter)
    {
        return parameter is int productId && productId > 0;
    }
}

// CommandManager.cs - Command coordinator
public class CommandManager
{
    private readonly Dictionary<string, ICommand> _commands;
    
    public CommandManager()
    {
        _commands = new Dictionary<string, ICommand>();
    }
    
    public void RegisterCommand(string commandName, ICommand command)
    {
        _commands[commandName] = command;
    }
    
    public void ExecuteCommand(string commandName, object parameter)
    {
        if (_commands.TryGetValue(commandName, out ICommand command))
        {
            if (command.CanExecute(parameter))
            {
                command.Execute(parameter);
            }
            else
            {
                throw new InvalidOperationException($"Cannot execute command: {commandName}");
            }
        }
        else
        {
            throw new ArgumentException($"Command not found: {commandName}");
        }
    }
    
    public bool CanExecuteCommand(string commandName, object parameter)
    {
        if (_commands.TryGetValue(commandName, out ICommand command))
        {
            return command.CanExecute(parameter);
        }
        return false;
    }
}

// Usage in page
public partial class ProductManagement : BasePage
{
    private CommandManager _commandManager;
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (_commandManager == null)
        {
            InitializeCommands();
        }
        
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    private void InitializeCommands()
    {
        var productService = new ProductService();
        _commandManager = new CommandManager();
        
        _commandManager.RegisterCommand("AddProduct", new AddProductCommand(productService));
        _commandManager.RegisterCommand("DeleteProduct", new DeleteProductCommand(productService));
    }
    
    protected void gvProducts_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        try
        {
            var parameter = e.CommandArgument;
            _commandManager.ExecuteCommand(e.CommandName, parameter);
            
            LoadProducts();
            ShowMessage("Operation completed successfully", MessageType.Success);
        }
        catch (Exception ex)
        {
            ShowMessage($"Error: {ex.Message}", MessageType.Error);
        }
    }
    
    protected void btnAdd_Click(object sender, EventArgs e)
    {
        var product = new Product
        {
            Name = txtName.Text,
            Price = decimal.Parse(txtPrice.Text),
            Description = txtDescription.Text
        };
        
        try
        {
            _commandManager.ExecuteCommand("AddProduct", product);
            LoadProducts();
            ClearForm();
            ShowMessage("Product added successfully", MessageType.Success);
        }
        catch (Exception ex)
        {
            ShowMessage($"Error adding product: {ex.Message}", MessageType.Error);
        }
    }
}
```

### 2. Event Aggregator Pattern

**Purpose**: Decouple event publishers from subscribers.

```csharp
// IEventAggregator.cs - Event aggregator interface
public interface IEventAggregator
{
    void Subscribe<T>(IEventHandler<T> handler) where T : class;
    void Unsubscribe<T>(IEventHandler<T> handler) where T : class;
    void Publish<T>(T eventData) where T : class;
}

public interface IEventHandler<T> where T : class
{
    void Handle(T eventData);
}

// EventAggregator.cs - Implementation
public class EventAggregator : IEventAggregator
{
    private readonly Dictionary<Type, List<object>> _handlers;
    
    public EventAggregator()
    {
        _handlers = new Dictionary<Type, List<object>>();
    }
    
    public void Subscribe<T>(IEventHandler<T> handler) where T : class
    {
        var eventType = typeof(T);
        
        if (!_handlers.ContainsKey(eventType))
        {
            _handlers[eventType] = new List<object>();
        }
        
        _handlers[eventType].Add(handler);
    }
    
    public void Unsubscribe<T>(IEventHandler<T> handler) where T : class
    {
        var eventType = typeof(T);
        
        if (_handlers.ContainsKey(eventType))
        {
            _handlers[eventType].Remove(handler);
        }
    }
    
    public void Publish<T>(T eventData) where T : class
    {
        var eventType = typeof(T);
        
        if (_handlers.ContainsKey(eventType))
        {
            foreach (var handler in _handlers[eventType].Cast<IEventHandler<T>>())
            {
                handler.Handle(eventData);
            }
        }
    }
}

// Event classes
public class ProductAddedEvent
{
    public Product Product { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.Now;
}

public class ProductDeletedEvent
{
    public int ProductId { get; set; }
    public DateTime Timestamp { get; set; } = DateTime.Now;
}

// Event handlers
public class ProductCacheHandler : IEventHandler<ProductAddedEvent>, IEventHandler<ProductDeletedEvent>
{
    public void Handle(ProductAddedEvent eventData)
    {
        // Clear product cache when new product added
        HttpContext.Current.Cache.Remove("AllProducts");
    }
    
    public void Handle(ProductDeletedEvent eventData)
    {
        // Clear product cache when product deleted
        HttpContext.Current.Cache.Remove("AllProducts");
        HttpContext.Current.Cache.Remove($"Product_{eventData.ProductId}");
    }
}

public class AuditLogHandler : IEventHandler<ProductAddedEvent>, IEventHandler<ProductDeletedEvent>
{
    public void Handle(ProductAddedEvent eventData)
    {
        LogActivity($"Product added: {eventData.Product.Name}");
    }
    
    public void Handle(ProductDeletedEvent eventData)
    {
        LogActivity($"Product deleted: {eventData.ProductId}");
    }
    
    private void LogActivity(string message)
    {
        // Log to database or file
        var log = new ActivityLog
        {
            Message = message,
            Timestamp = DateTime.Now,
            UserId = SessionHelper.UserId ?? 0
        };
        
        // Save log
    }
}

// Usage in application
public class Global : HttpApplication
{
    public static IEventAggregator EventAggregator { get; private set; }
    
    protected void Application_Start()
    {
        EventAggregator = new EventAggregator();
        
        // Register event handlers
        EventAggregator.Subscribe<ProductAddedEvent>(new ProductCacheHandler());
        EventAggregator.Subscribe<ProductDeletedEvent>(new ProductCacheHandler());
        EventAggregator.Subscribe<ProductAddedEvent>(new AuditLogHandler());
        EventAggregator.Subscribe<ProductDeletedEvent>(new AuditLogHandler());
    }
}

// Usage in pages
public partial class ProductManagement : BasePage
{
    protected void btnAdd_Click(object sender, EventArgs e)
    {
        var product = CreateProductFromForm();
        productService.AddProduct(product);
        
        // Publish event
        Global.EventAggregator.Publish(new ProductAddedEvent { Product = product });
        
        LoadProducts();
        ShowMessage("Product added successfully", MessageType.Success);
    }
    
    protected void DeleteProduct(int productId)
    {
        productService.DeleteProduct(productId);
        
        // Publish event
        Global.EventAggregator.Publish(new ProductDeletedEvent { ProductId = productId });
        
        LoadProducts();
        ShowMessage("Product deleted successfully", MessageType.Success);
    }
}
```

## Security Patterns

### 1. Authorization Wrapper Pattern

**Purpose**: Centralize authorization logic across pages.

```csharp
// AuthorizationManager.cs - Authorization logic
public static class AuthorizationManager
{
    public static bool IsAuthorized(string[] requiredRoles = null, string[] requiredPermissions = null)
    {
        if (!HttpContext.Current.User.Identity.IsAuthenticated)
        {
            return false;
        }
        
        // Check roles
        if (requiredRoles != null && requiredRoles.Length > 0)
        {
            foreach (var role in requiredRoles)
            {
                if (HttpContext.Current.User.IsInRole(role))
                {
                    return CheckPermissions(requiredPermissions);
                }
            }
            return false;
        }
        
        return CheckPermissions(requiredPermissions);
    }
    
    private static bool CheckPermissions(string[] requiredPermissions)
    {
        if (requiredPermissions == null || requiredPermissions.Length == 0)
        {
            return true;
        }
        
        var userPermissions = GetUserPermissions();
        return requiredPermissions.All(p => userPermissions.Contains(p));
    }
    
    private static List<string> GetUserPermissions()
    {
        // Get from cache or database
        var cacheKey = $"UserPermissions_{HttpContext.Current.User.Identity.Name}";
        var permissions = HttpContext.Current.Cache[cacheKey] as List<string>;
        
        if (permissions == null)
        {
            permissions = LoadUserPermissions();
            HttpContext.Current.Cache.Insert(cacheKey, permissions, null, 
                DateTime.Now.AddMinutes(30), TimeSpan.Zero);
        }
        
        return permissions;
    }
    
    private static List<string> LoadUserPermissions()
    {
        // Load from database
        // Implementation depends on your security model
        return new List<string>();
    }
    
    public static void RedirectIfUnauthorized(string[] requiredRoles = null, string[] requiredPermissions = null)
    {
        if (!IsAuthorized(requiredRoles, requiredPermissions))
        {
            if (!HttpContext.Current.User.Identity.IsAuthenticated)
            {
                FormsAuthentication.RedirectToLoginPage();
            }
            else
            {
                HttpContext.Current.Response.Redirect("~/Unauthorized.aspx");
            }
        }
    }
}

// SecureBasePage.cs - Secure base page
public class SecureBasePage : BasePage
{
    protected virtual string[] RequiredRoles => null;
    protected virtual string[] RequiredPermissions => null;
    
    protected override void OnInit(EventArgs e)
    {
        base.OnInit(e);
        
        AuthorizationManager.RedirectIfUnauthorized(RequiredRoles, RequiredPermissions);
    }
}

// Usage in pages
public partial class AdminPanel : SecureBasePage
{
    protected override string[] RequiredRoles => new[] { "Administrator", "SuperUser" };
    protected override string[] RequiredPermissions => new[] { "ManageUsers", "ManageSystem" };
    
    protected void Page_Load(object sender, EventArgs e)
    {
        // Page content only accessible to authorized users
        if (!IsPostBack)
        {
            LoadAdminData();
        }
    }
}
```

### 2. Input Validation Pattern

**Purpose**: Standardize input validation and sanitization.

```csharp
// ValidationHelper.cs - Validation utilities
public static class ValidationHelper
{
    public static string SanitizeInput(string input)
    {
        if (string.IsNullOrEmpty(input))
            return string.Empty;
            
        // HTML encode to prevent XSS
        return HttpUtility.HtmlEncode(input.Trim());
    }
    
    public static string SanitizeHtml(string html)
    {
        if (string.IsNullOrEmpty(html))
            return string.Empty;
            
        // Use HtmlAgilityPack or similar for advanced HTML sanitization
        // This is a basic example
        return Regex.Replace(html, @"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", 
            string.Empty, RegexOptions.IgnoreCase);
    }
    
    public static bool IsValidEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return false;
            
        var pattern = @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";
        return Regex.IsMatch(email, pattern);
    }
    
    public static bool IsValidPhoneNumber(string phone)
    {
        if (string.IsNullOrWhiteSpace(phone))
            return false;
            
        var pattern = @"^\+?[\d\s\-\(\)]{10,}$";
        return Regex.IsMatch(phone, pattern);
    }
    
    public static bool IsSqlSafe(string input)
    {
        if (string.IsNullOrEmpty(input))
            return true;
            
        var dangerousKeywords = new[] { "drop", "delete", "insert", "update", "exec", "execute", "sp_", "xp_" };
        var lowerInput = input.ToLower();
        
        return !dangerousKeywords.Any(keyword => lowerInput.Contains(keyword));
    }
}

// ValidatedPage.cs - Page with built-in validation
public class ValidatedPage : SecureBasePage
{
    protected string GetSafeInput(string controlId)
    {
        var control = FindControl(controlId) as TextBox;
        if (control != null)
        {
            return ValidationHelper.SanitizeInput(control.Text);
        }
        
        return string.Empty;
    }
    
    protected bool ValidateForm(params string[] requiredFields)
    {
        var isValid = true;
        var errorMessages = new List<string>();
        
        foreach (var fieldId in requiredFields)
        {
            var value = GetSafeInput(fieldId);
            if (string.IsNullOrEmpty(value))
            {
                isValid = false;
                errorMessages.Add($"{fieldId} is required");
            }
        }
        
        if (!isValid)
        {
            ShowMessage(string.Join(", ", errorMessages), MessageType.Error);
        }
        
        return isValid;
    }
    
    protected bool ValidateEmail(string emailControlId)
    {
        var email = GetSafeInput(emailControlId);
        if (!ValidationHelper.IsValidEmail(email))
        {
            ShowMessage("Please enter a valid email address", MessageType.Error);
            return false;
        }
        
        return true;
    }
}

// Usage in form page
public partial class ContactForm : ValidatedPage
{
    protected void btnSubmit_Click(object sender, EventArgs e)
    {
        if (!ValidateForm("txtName", "txtEmail", "txtMessage"))
        {
            return;
        }
        
        if (!ValidateEmail("txtEmail"))
        {
            return;
        }
        
        var contact = new ContactSubmission
        {
            Name = GetSafeInput("txtName"),
            Email = GetSafeInput("txtEmail"),
            Message = GetSafeInput("txtMessage"),
            SubmissionDate = DateTime.Now
        };
        
        SaveContact(contact);
        ShowMessage("Thank you for your message!", MessageType.Success);
        ClearForm();
    }
}
```

## Anti-Patterns to Avoid

### 1. Tight Coupling to Page Lifecycle

**Problem**: Business logic embedded in page events.

```csharp
// ❌ BAD: Business logic in page events
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        // Database connection directly in page
        using (var conn = new SqlConnection(connectionString))
        {
            conn.Open();
            var cmd = new SqlCommand("SELECT * FROM Users", conn);
            var reader = cmd.ExecuteReader();
            
            var users = new List<User>();
            while (reader.Read())
            {
                // Direct data mapping in page
                users.Add(new User
                {
                    Id = (int)reader["Id"],
                    Name = reader["Name"].ToString()
                });
            }
            
            GridView1.DataSource = users;
            GridView1.DataBind();
        }
    }
}
```

```csharp
// ✅ GOOD: Business logic in separate layer
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        LoadUsers();
    }
}

private void LoadUsers()
{
    try
    {
        var users = _userService.GetUsers();
        GridView1.DataSource = users;
        GridView1.DataBind();
    }
    catch (Exception ex)
    {
        ShowMessage($"Error loading users: {ex.Message}", MessageType.Error);
    }
}
```

### 2. ViewState Abuse

**Problem**: Storing large objects in ViewState.

```csharp
// ❌ BAD: Large objects in ViewState
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        // Storing large dataset in ViewState
        ViewState["AllUsers"] = GetAllUsers(); // Could be thousands of records
        ViewState["ComplexObject"] = GetComplexBusinessObject();
    }
}
```

```csharp
// ✅ GOOD: Minimal ViewState usage
protected void Page_Load(object sender, EventArgs e)
{
    if (!IsPostBack)
    {
        // Store only essential state
        ViewState["CurrentPage"] = 0;
        ViewState["SortDirection"] = "ASC";
        LoadCurrentPageData();
    }
}

private void LoadCurrentPageData()
{
    var currentPage = (int)ViewState["CurrentPage"];
    var users = _userService.GetUsers(currentPage, PageSize);
    GridView1.DataSource = users;
    GridView1.DataBind();
}
```

### 3. Session State Overuse

**Problem**: Storing excessive data in session.

```csharp
// ❌ BAD: Session abuse
protected void LoadUserData()
{
    // Storing too much in session
    Session["AllUsers"] = GetAllUsers();
    Session["AllProducts"] = GetAllProducts();
    Session["AllOrders"] = GetAllOrders();
    Session["ComplexReport"] = GenerateComplexReport();
}
```

```csharp
// ✅ GOOD: Minimal session usage with caching
protected void LoadUserData()
{
    // Store only user-specific state
    Session["UserId"] = currentUserId;
    Session["UserName"] = currentUserName;
    
    // Use application cache for shared data
    if (Cache["AllProducts"] == null)
    {
        Cache.Insert("AllProducts", GetAllProducts(), null, 
            DateTime.Now.AddMinutes(30), TimeSpan.Zero);
    }
}
```

### 4. Postback Proliferation

**Problem**: Excessive postbacks for simple interactions.

```aspx
<%-- ❌ BAD: Unnecessary postbacks --%>
<asp:DropDownList ID="ddlCategory" runat="server" 
    AutoPostBack="true" OnSelectedIndexChanged="ddlCategory_SelectedIndexChanged" />
<asp:DropDownList ID="ddlSubCategory" runat="server" 
    AutoPostBack="true" OnSelectedIndexChanged="ddlSubCategory_SelectedIndexChanged" />
<asp:TextBox ID="txtSearch" runat="server" 
    AutoPostBack="true" OnTextChanged="txtSearch_TextChanged" />
```

```aspx
<%-- ✅ GOOD: Client-side interactions where appropriate --%>
<asp:DropDownList ID="ddlCategory" runat="server" 
    onchange="updateSubCategories(this.value);" />
<asp:DropDownList ID="ddlSubCategory" runat="server" />
<asp:TextBox ID="txtSearch" runat="server" 
    placeholder="Enter search term..." />
<asp:Button ID="btnSearch" runat="server" Text="Search" 
    OnClick="btnSearch_Click" />

<script type="text/javascript">
    function updateSubCategories(categoryId) {
        // AJAX call to update subcategories
        PageMethods.GetSubCategories(categoryId, onSubCategoriesLoaded);
    }
    
    function onSubCategoriesLoaded(result) {
        var ddlSub = document.getElementById('<%= ddlSubCategory.ClientID %>');
        ddlSub.innerHTML = result;
    }
</script>
```

This catalog provides comprehensive examples of both effective patterns and anti-patterns to guide WebForms development and assessment activities.