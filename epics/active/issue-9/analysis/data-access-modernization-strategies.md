# Data Access Layer Modernization Strategies

## Overview

Legacy WebForms applications often contain outdated data access patterns that hinder maintainability, testability, and performance. This guide provides comprehensive strategies for modernizing data access layers during WebForms migration.

## Legacy Data Access Pattern Analysis

### Common Anti-Patterns in WebForms

#### 1. Direct Database Access in Code-Behind
```csharp
// Anti-pattern: Direct database access in page
public partial class ProductList : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadProducts();
        }
    }
    
    private void LoadProducts()
    {
        var connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;
        using (var connection = new SqlConnection(connectionString))
        {
            connection.Open();
            var command = new SqlCommand(@"
                SELECT p.Id, p.Name, p.Price, c.Name as CategoryName
                FROM Products p 
                INNER JOIN Categories c ON p.CategoryId = c.Id
                WHERE p.IsActive = 1
                ORDER BY p.Name", connection);
                
            var reader = command.ExecuteReader();
            var products = new List<Product>();
            
            while (reader.Read())
            {
                products.Add(new Product
                {
                    Id = (int)reader["Id"],
                    Name = reader["Name"].ToString(),
                    Price = (decimal)reader["Price"],
                    CategoryName = reader["CategoryName"].ToString()
                });
            }
            
            GridView1.DataSource = products;
            GridView1.DataBind();
        }
    }
    
    protected void btnDelete_Click(object sender, EventArgs e)
    {
        var productId = Convert.ToInt32(((Button)sender).CommandArgument);
        var connectionString = ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString;
        
        using (var connection = new SqlConnection(connectionString))
        {
            connection.Open();
            var command = new SqlCommand("DELETE FROM Products WHERE Id = @Id", connection);
            command.Parameters.AddWithValue("@Id", productId);
            command.ExecuteNonQuery();
        }
        
        LoadProducts(); // Reload after delete
    }
}
```

#### 2. Dataset/DataTable Heavy Usage
```csharp
// Anti-pattern: DataSet/DataTable usage
public partial class OrderManagement : Page
{
    private void LoadOrderData()
    {
        var dataSet = new DataSet();
        var adapter = new SqlDataAdapter(@"
            SELECT o.Id, o.OrderDate, o.TotalAmount, c.Name as CustomerName
            FROM Orders o
            INNER JOIN Customers c ON o.CustomerId = c.Id
            ORDER BY o.OrderDate DESC", GetConnectionString());
            
        adapter.Fill(dataSet, "Orders");
        
        Session["OrderDataSet"] = dataSet;
        
        GridView1.DataSource = dataSet.Tables["Orders"];
        GridView1.DataBind();
    }
    
    protected void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
    {
        var dataSet = (DataSet)Session["OrderDataSet"];
        var row = dataSet.Tables["Orders"].Rows[e.RowIndex];
        
        row["TotalAmount"] = Convert.ToDecimal(((TextBox)GridView1.Rows[e.RowIndex].Cells[2].Controls[0]).Text);
        
        var commandBuilder = new SqlCommandBuilder(new SqlDataAdapter());
        var updateAdapter = new SqlDataAdapter();
        updateAdapter.UpdateCommand = commandBuilder.GetUpdateCommand();
        updateAdapter.Update(dataSet, "Orders");
        
        GridView1.EditIndex = -1;
        LoadOrderData();
    }
}
```

## Modern Data Access Architecture

### Repository Pattern Implementation

#### 1. Base Repository Interface
```csharp
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate);
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
    Task<bool> ExistsAsync(int id);
    Task<int> CountAsync();
    Task<int> CountAsync(Expression<Func<T, bool>> predicate);
}

public interface IUnitOfWork : IDisposable
{
    IProductRepository Products { get; }
    ICategoryRepository Categories { get; }
    IOrderRepository Orders { get; }
    ICustomerRepository Customers { get; }
    
    Task<int> SaveChangesAsync();
    Task BeginTransactionAsync();
    Task CommitTransactionAsync();
    Task RollbackTransactionAsync();
}
```

#### 2. Entity Framework Core Implementation
```csharp
// DbContext
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }
    
    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }
    public DbSet<Order> Orders { get; set; }
    public DbSet<Customer> Customers { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure entities
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(255);
            entity.Property(e => e.Price).HasPrecision(18, 2);
            entity.HasOne(e => e.Category).WithMany(c => c.Products).HasForeignKey(e => e.CategoryId);
            entity.HasIndex(e => e.Name);
        });
        
        modelBuilder.Entity<Category>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(100);
            entity.HasIndex(e => e.Name).IsUnique();
        });
        
        // Configure relationships, indexes, etc.
        base.OnModelCreating(modelBuilder);
    }
}

// Generic Repository
public class Repository<T> : IRepository<T> where T : class
{
    protected readonly ApplicationDbContext _context;
    protected readonly DbSet<T> _dbSet;
    private readonly ILogger<Repository<T>> _logger;
    
    public Repository(ApplicationDbContext context, ILogger<Repository<T>> logger)
    {
        _context = context;
        _dbSet = context.Set<T>();
        _logger = logger;
    }
    
    public virtual async Task<T> GetByIdAsync(int id)
    {
        try
        {
            return await _dbSet.FindAsync(id);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving entity by ID: {Id}", id);
            throw;
        }
    }
    
    public virtual async Task<IEnumerable<T>> GetAllAsync()
    {
        try
        {
            return await _dbSet.ToListAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving all entities");
            throw;
        }
    }
    
    public virtual async Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate)
    {
        try
        {
            return await _dbSet.Where(predicate).ToListAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error finding entities with predicate");
            throw;
        }
    }
    
    public virtual async Task<T> AddAsync(T entity)
    {
        try
        {
            var result = await _dbSet.AddAsync(entity);
            return result.Entity;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error adding entity");
            throw;
        }
    }
    
    public virtual async Task UpdateAsync(T entity)
    {
        try
        {
            _dbSet.Update(entity);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating entity");
            throw;
        }
    }
    
    public virtual async Task DeleteAsync(int id)
    {
        try
        {
            var entity = await GetByIdAsync(id);
            if (entity != null)
            {
                _dbSet.Remove(entity);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting entity with ID: {Id}", id);
            throw;
        }
    }
    
    public virtual async Task<bool> ExistsAsync(int id)
    {
        try
        {
            return await _dbSet.FindAsync(id) != null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error checking entity existence for ID: {Id}", id);
            throw;
        }
    }
    
    public virtual async Task<int> CountAsync()
    {
        try
        {
            return await _dbSet.CountAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error counting entities");
            throw;
        }
    }
    
    public virtual async Task<int> CountAsync(Expression<Func<T, bool>> predicate)
    {
        try
        {
            return await _dbSet.CountAsync(predicate);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error counting entities with predicate");
            throw;
        }
    }
}

// Specific Repository Implementation
public interface IProductRepository : IRepository<Product>
{
    Task<IEnumerable<Product>> GetProductsByCategoryAsync(int categoryId);
    Task<IEnumerable<Product>> GetProductsByPriceRangeAsync(decimal minPrice, decimal maxPrice);
    Task<IEnumerable<Product>> SearchProductsAsync(string searchTerm);
    Task<PagedResult<Product>> GetProductsPagedAsync(int pageIndex, int pageSize, string sortColumn, bool ascending);
}

public class ProductRepository : Repository<Product>, IProductRepository
{
    public ProductRepository(ApplicationDbContext context, ILogger<ProductRepository> logger) 
        : base(context, logger) { }
    
    public async Task<IEnumerable<Product>> GetProductsByCategoryAsync(int categoryId)
    {
        return await _dbSet
            .Include(p => p.Category)
            .Where(p => p.CategoryId == categoryId && p.IsActive)
            .OrderBy(p => p.Name)
            .ToListAsync();
    }
    
    public async Task<IEnumerable<Product>> GetProductsByPriceRangeAsync(decimal minPrice, decimal maxPrice)
    {
        return await _dbSet
            .Include(p => p.Category)
            .Where(p => p.Price >= minPrice && p.Price <= maxPrice && p.IsActive)
            .OrderBy(p => p.Price)
            .ToListAsync();
    }
    
    public async Task<IEnumerable<Product>> SearchProductsAsync(string searchTerm)
    {
        return await _dbSet
            .Include(p => p.Category)
            .Where(p => (p.Name.Contains(searchTerm) || p.Description.Contains(searchTerm)) && p.IsActive)
            .OrderBy(p => p.Name)
            .ToListAsync();
    }
    
    public async Task<PagedResult<Product>> GetProductsPagedAsync(int pageIndex, int pageSize, string sortColumn, bool ascending)
    {
        var query = _dbSet.Include(p => p.Category).Where(p => p.IsActive);
        
        // Apply sorting
        query = sortColumn.ToLower() switch
        {
            "name" => ascending ? query.OrderBy(p => p.Name) : query.OrderByDescending(p => p.Name),
            "price" => ascending ? query.OrderBy(p => p.Price) : query.OrderByDescending(p => p.Price),
            "category" => ascending ? query.OrderBy(p => p.Category.Name) : query.OrderByDescending(p => p.Category.Name),
            _ => query.OrderBy(p => p.Id)
        };
        
        var totalCount = await query.CountAsync();
        var items = await query
            .Skip(pageIndex * pageSize)
            .Take(pageSize)
            .ToListAsync();
        
        return new PagedResult<Product>
        {
            Items = items,
            TotalCount = totalCount,
            PageIndex = pageIndex,
            PageSize = pageSize,
            TotalPages = (int)Math.Ceiling((double)totalCount / pageSize)
        };
    }
}

// Unit of Work Implementation
public class UnitOfWork : IUnitOfWork
{
    private readonly ApplicationDbContext _context;
    private readonly ILogger<UnitOfWork> _logger;
    private IDbContextTransaction _transaction;
    
    public UnitOfWork(
        ApplicationDbContext context,
        IProductRepository productRepository,
        ICategoryRepository categoryRepository,
        IOrderRepository orderRepository,
        ICustomerRepository customerRepository,
        ILogger<UnitOfWork> logger)
    {
        _context = context;
        _logger = logger;
        Products = productRepository;
        Categories = categoryRepository;
        Orders = orderRepository;
        Customers = customerRepository;
    }
    
    public IProductRepository Products { get; }
    public ICategoryRepository Categories { get; }
    public IOrderRepository Orders { get; }
    public ICustomerRepository Customers { get; }
    
    public async Task<int> SaveChangesAsync()
    {
        try
        {
            return await _context.SaveChangesAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error saving changes to database");
            throw;
        }
    }
    
    public async Task BeginTransactionAsync()
    {
        try
        {
            _transaction = await _context.Database.BeginTransactionAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error beginning database transaction");
            throw;
        }
    }
    
    public async Task CommitTransactionAsync()
    {
        try
        {
            if (_transaction != null)
            {
                await _transaction.CommitAsync();
                await _transaction.DisposeAsync();
                _transaction = null;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error committing database transaction");
            await RollbackTransactionAsync();
            throw;
        }
    }
    
    public async Task RollbackTransactionAsync()
    {
        try
        {
            if (_transaction != null)
            {
                await _transaction.RollbackAsync();
                await _transaction.DisposeAsync();
                _transaction = null;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error rolling back database transaction");
            throw;
        }
    }
    
    public void Dispose()
    {
        _transaction?.Dispose();
        _context?.Dispose();
    }
}
```

#### 3. Service Layer Implementation
```csharp
public interface IProductService
{
    Task<ProductDto> GetProductByIdAsync(int id);
    Task<IEnumerable<ProductDto>> GetProductsAsync();
    Task<IEnumerable<ProductDto>> GetProductsByCategoryAsync(int categoryId);
    Task<PagedResult<ProductDto>> GetProductsPagedAsync(ProductSearchCriteria criteria);
    Task<ProductDto> CreateProductAsync(CreateProductDto createProductDto);
    Task<ProductDto> UpdateProductAsync(int id, UpdateProductDto updateProductDto);
    Task DeleteProductAsync(int id);
    Task<bool> ProductExistsAsync(int id);
}

public class ProductService : IProductService
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly ILogger<ProductService> _logger;
    private readonly ICacheService _cacheService;
    
    public ProductService(
        IUnitOfWork unitOfWork, 
        IMapper mapper, 
        ILogger<ProductService> logger,
        ICacheService cacheService)
    {
        _unitOfWork = unitOfWork;
        _mapper = mapper;
        _logger = logger;
        _cacheService = cacheService;
    }
    
    public async Task<ProductDto> GetProductByIdAsync(int id)
    {
        try
        {
            var cacheKey = $"product:{id}";
            var cachedProduct = await _cacheService.GetAsync<ProductDto>(cacheKey);
            
            if (cachedProduct != null)
            {
                return cachedProduct;
            }
            
            var product = await _unitOfWork.Products.GetByIdAsync(id);
            if (product == null)
            {
                throw new NotFoundException($"Product with ID {id} not found");
            }
            
            var productDto = _mapper.Map<ProductDto>(product);
            
            // Cache for 15 minutes
            await _cacheService.SetAsync(cacheKey, productDto, TimeSpan.FromMinutes(15));
            
            return productDto;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product by ID: {ProductId}", id);
            throw;
        }
    }
    
    public async Task<PagedResult<ProductDto>> GetProductsPagedAsync(ProductSearchCriteria criteria)
    {
        try
        {
            var pagedProducts = await _unitOfWork.Products.GetProductsPagedAsync(
                criteria.PageIndex,
                criteria.PageSize,
                criteria.SortColumn,
                criteria.SortAscending
            );
            
            var productDtos = _mapper.Map<List<ProductDto>>(pagedProducts.Items);
            
            return new PagedResult<ProductDto>
            {
                Items = productDtos,
                TotalCount = pagedProducts.TotalCount,
                PageIndex = pagedProducts.PageIndex,
                PageSize = pagedProducts.PageSize,
                TotalPages = pagedProducts.TotalPages
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving paged products");
            throw;
        }
    }
    
    public async Task<ProductDto> CreateProductAsync(CreateProductDto createProductDto)
    {
        try
        {
            // Validate business rules
            await ValidateCreateProductAsync(createProductDto);
            
            await _unitOfWork.BeginTransactionAsync();
            
            var product = _mapper.Map<Product>(createProductDto);
            product.CreatedAt = DateTime.UtcNow;
            product.IsActive = true;
            
            var createdProduct = await _unitOfWork.Products.AddAsync(product);
            await _unitOfWork.SaveChangesAsync();
            
            await _unitOfWork.CommitTransactionAsync();
            
            // Invalidate related cache
            await _cacheService.RemovePatternAsync("product:*");
            
            var result = _mapper.Map<ProductDto>(createdProduct);
            
            _logger.LogInformation("Product created successfully: {ProductId}", result.Id);
            
            return result;
        }
        catch (Exception ex)
        {
            await _unitOfWork.RollbackTransactionAsync();
            _logger.LogError(ex, "Error creating product");
            throw;
        }
    }
    
    public async Task<ProductDto> UpdateProductAsync(int id, UpdateProductDto updateProductDto)
    {
        try
        {
            var existingProduct = await _unitOfWork.Products.GetByIdAsync(id);
            if (existingProduct == null)
            {
                throw new NotFoundException($"Product with ID {id} not found");
            }
            
            await ValidateUpdateProductAsync(id, updateProductDto);
            
            await _unitOfWork.BeginTransactionAsync();
            
            _mapper.Map(updateProductDto, existingProduct);
            existingProduct.UpdatedAt = DateTime.UtcNow;
            
            await _unitOfWork.Products.UpdateAsync(existingProduct);
            await _unitOfWork.SaveChangesAsync();
            
            await _unitOfWork.CommitTransactionAsync();
            
            // Invalidate cache
            await _cacheService.RemoveAsync($"product:{id}");
            await _cacheService.RemovePatternAsync("product:*");
            
            var result = _mapper.Map<ProductDto>(existingProduct);
            
            _logger.LogInformation("Product updated successfully: {ProductId}", id);
            
            return result;
        }
        catch (Exception ex)
        {
            await _unitOfWork.RollbackTransactionAsync();
            _logger.LogError(ex, "Error updating product: {ProductId}", id);
            throw;
        }
    }
    
    private async Task ValidateCreateProductAsync(CreateProductDto createProductDto)
    {
        // Check if category exists
        var categoryExists = await _unitOfWork.Categories.ExistsAsync(createProductDto.CategoryId);
        if (!categoryExists)
        {
            throw new ValidationException("Invalid category ID");
        }
        
        // Check for duplicate product names
        var existingProducts = await _unitOfWork.Products.FindAsync(p => p.Name == createProductDto.Name);
        if (existingProducts.Any())
        {
            throw new ValidationException("Product name already exists");
        }
    }
}
```

### Dapper Implementation for Performance-Critical Scenarios

#### 1. Dapper Repository for High-Performance Operations
```csharp
public interface IProductQueryRepository
{
    Task<ProductDto> GetProductByIdAsync(int id);
    Task<IEnumerable<ProductDto>> GetProductsAsync(ProductQueryFilter filter);
    Task<PagedResult<ProductDto>> GetProductsPagedAsync(ProductPagedQuery query);
    Task<IEnumerable<ProductStatDto>> GetProductStatisticsAsync();
}

public class DapperProductQueryRepository : IProductQueryRepository
{
    private readonly IDbConnectionFactory _connectionFactory;
    private readonly ILogger<DapperProductQueryRepository> _logger;
    
    public DapperProductQueryRepository(
        IDbConnectionFactory connectionFactory,
        ILogger<DapperProductQueryRepository> logger)
    {
        _connectionFactory = connectionFactory;
        _logger = logger;
    }
    
    public async Task<ProductDto> GetProductByIdAsync(int id)
    {
        try
        {
            using var connection = await _connectionFactory.CreateConnectionAsync();
            
            const string sql = @"
                SELECT p.Id, p.Name, p.Description, p.Price, p.CategoryId, p.IsActive,
                       c.Name as CategoryName
                FROM Products p
                INNER JOIN Categories c ON p.CategoryId = c.Id
                WHERE p.Id = @Id";
            
            return await connection.QueryFirstOrDefaultAsync<ProductDto>(sql, new { Id = id });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product by ID: {ProductId}", id);
            throw;
        }
    }
    
    public async Task<IEnumerable<ProductDto>> GetProductsAsync(ProductQueryFilter filter)
    {
        try
        {
            using var connection = await _connectionFactory.CreateConnectionAsync();
            
            var sqlBuilder = new SqlBuilder();
            var template = sqlBuilder.AddTemplate(@"
                SELECT p.Id, p.Name, p.Description, p.Price, p.CategoryId, p.IsActive,
                       c.Name as CategoryName
                FROM Products p
                INNER JOIN Categories c ON p.CategoryId = c.Id
                /**where**/
                /**orderby**/");
            
            // Build dynamic WHERE clause
            if (filter.CategoryId.HasValue)
            {
                sqlBuilder.Where("p.CategoryId = @CategoryId", new { CategoryId = filter.CategoryId });
            }
            
            if (filter.MinPrice.HasValue)
            {
                sqlBuilder.Where("p.Price >= @MinPrice", new { MinPrice = filter.MinPrice });
            }
            
            if (filter.MaxPrice.HasValue)
            {
                sqlBuilder.Where("p.Price <= @MaxPrice", new { MaxPrice = filter.MaxPrice });
            }
            
            if (!string.IsNullOrEmpty(filter.SearchTerm))
            {
                sqlBuilder.Where("(p.Name LIKE @SearchTerm OR p.Description LIKE @SearchTerm)", 
                    new { SearchTerm = $"%{filter.SearchTerm}%" });
            }
            
            sqlBuilder.Where("p.IsActive = 1");
            
            // Build dynamic ORDER BY clause
            var orderBy = filter.SortColumn?.ToLower() switch
            {
                "name" => filter.SortAscending ? "p.Name" : "p.Name DESC",
                "price" => filter.SortAscending ? "p.Price" : "p.Price DESC",
                "category" => filter.SortAscending ? "c.Name" : "c.Name DESC",
                _ => "p.Id"
            };
            
            sqlBuilder.OrderBy(orderBy);
            
            return await connection.QueryAsync<ProductDto>(template.RawSql, template.Parameters);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving products with filter");
            throw;
        }
    }
    
    public async Task<PagedResult<ProductDto>> GetProductsPagedAsync(ProductPagedQuery query)
    {
        try
        {
            using var connection = await _connectionFactory.CreateConnectionAsync();
            
            // Get total count
            const string countSql = @"
                SELECT COUNT(*)
                FROM Products p
                INNER JOIN Categories c ON p.CategoryId = c.Id
                WHERE p.IsActive = 1";
            
            var totalCount = await connection.QueryFirstOrDefaultAsync<int>(countSql);
            
            // Get paged data
            var offset = query.PageIndex * query.PageSize;
            var sql = $@"
                SELECT p.Id, p.Name, p.Description, p.Price, p.CategoryId, p.IsActive,
                       c.Name as CategoryName
                FROM Products p
                INNER JOIN Categories c ON p.CategoryId = c.Id
                WHERE p.IsActive = 1
                ORDER BY {GetOrderByClause(query.SortColumn, query.SortAscending)}
                OFFSET @Offset ROWS
                FETCH NEXT @PageSize ROWS ONLY";
            
            var products = await connection.QueryAsync<ProductDto>(sql, new 
            { 
                Offset = offset, 
                PageSize = query.PageSize 
            });
            
            return new PagedResult<ProductDto>
            {
                Items = products.ToList(),
                TotalCount = totalCount,
                PageIndex = query.PageIndex,
                PageSize = query.PageSize,
                TotalPages = (int)Math.Ceiling((double)totalCount / query.PageSize)
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving paged products");
            throw;
        }
    }
    
    public async Task<IEnumerable<ProductStatDto>> GetProductStatisticsAsync()
    {
        try
        {
            using var connection = await _connectionFactory.CreateConnectionAsync();
            
            const string sql = @"
                SELECT 
                    c.Name as CategoryName,
                    COUNT(p.Id) as ProductCount,
                    AVG(p.Price) as AveragePrice,
                    MIN(p.Price) as MinPrice,
                    MAX(p.Price) as MaxPrice,
                    SUM(CASE WHEN p.IsActive = 1 THEN 1 ELSE 0 END) as ActiveCount
                FROM Categories c
                LEFT JOIN Products p ON c.Id = p.CategoryId
                GROUP BY c.Id, c.Name
                ORDER BY c.Name";
            
            return await connection.QueryAsync<ProductStatDto>(sql);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving product statistics");
            throw;
        }
    }
    
    private string GetOrderByClause(string sortColumn, bool ascending)
    {
        var direction = ascending ? "ASC" : "DESC";
        
        return sortColumn?.ToLower() switch
        {
            "name" => $"p.Name {direction}",
            "price" => $"p.Price {direction}",
            "category" => $"c.Name {direction}",
            _ => "p.Id ASC"
        };
    }
}

// Connection factory for Dapper
public interface IDbConnectionFactory
{
    Task<IDbConnection> CreateConnectionAsync();
    IDbConnection CreateConnection();
}

public class SqlConnectionFactory : IDbConnectionFactory
{
    private readonly string _connectionString;
    
    public SqlConnectionFactory(string connectionString)
    {
        _connectionString = connectionString;
    }
    
    public async Task<IDbConnection> CreateConnectionAsync()
    {
        var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync();
        return connection;
    }
    
    public IDbConnection CreateConnection()
    {
        var connection = new SqlConnection(_connectionString);
        connection.Open();
        return connection;
    }
}
```

### CQRS (Command Query Responsibility Segregation) Implementation

#### 1. Command and Query Separation
```csharp
// Commands (Write operations)
public interface ICommand<TResponse>
{
    // Marker interface
}

public interface ICommandHandler<TCommand, TResponse> where TCommand : ICommand<TResponse>
{
    Task<TResponse> HandleAsync(TCommand command);
}

// Queries (Read operations)
public interface IQuery<TResponse>
{
    // Marker interface
}

public interface IQueryHandler<TQuery, TResponse> where TQuery : IQuery<TResponse>
{
    Task<TResponse> HandleAsync(TQuery query);
}

// Mediator pattern implementation
public interface IMediator
{
    Task<TResponse> SendAsync<TResponse>(ICommand<TResponse> command);
    Task<TResponse> SendAsync<TResponse>(IQuery<TResponse> query);
}

public class Mediator : IMediator
{
    private readonly IServiceProvider _serviceProvider;
    
    public Mediator(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public async Task<TResponse> SendAsync<TResponse>(ICommand<TResponse> command)
    {
        var commandType = command.GetType();
        var handlerType = typeof(ICommandHandler<,>).MakeGenericType(commandType, typeof(TResponse));
        var handler = _serviceProvider.GetService(handlerType);
        
        if (handler == null)
        {
            throw new InvalidOperationException($"No handler found for command {commandType.Name}");
        }
        
        var method = handlerType.GetMethod("HandleAsync");
        var task = (Task<TResponse>)method.Invoke(handler, new object[] { command });
        
        return await task;
    }
    
    public async Task<TResponse> SendAsync<TResponse>(IQuery<TResponse> query)
    {
        var queryType = query.GetType();
        var handlerType = typeof(IQueryHandler<,>).MakeGenericType(queryType, typeof(TResponse));
        var handler = _serviceProvider.GetService(handlerType);
        
        if (handler == null)
        {
            throw new InvalidOperationException($"No handler found for query {queryType.Name}");
        }
        
        var method = handlerType.GetMethod("HandleAsync");
        var task = (Task<TResponse>)method.Invoke(handler, new object[] { query });
        
        return await task;
    }
}

// Example Commands
public class CreateProductCommand : ICommand<CreateProductResult>
{
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal Price { get; set; }
    public int CategoryId { get; set; }
}

public class CreateProductResult
{
    public bool Success { get; set; }
    public int ProductId { get; set; }
    public string Message { get; set; }
}

public class CreateProductCommandHandler : ICommandHandler<CreateProductCommand, CreateProductResult>
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IValidator<CreateProductCommand> _validator;
    private readonly ILogger<CreateProductCommandHandler> _logger;
    
    public async Task<CreateProductResult> HandleAsync(CreateProductCommand command)
    {
        try
        {
            // Validate command
            var validationResult = await _validator.ValidateAsync(command);
            if (!validationResult.IsValid)
            {
                return new CreateProductResult
                {
                    Success = false,
                    Message = string.Join(", ", validationResult.Errors.Select(e => e.ErrorMessage))
                };
            }
            
            await _unitOfWork.BeginTransactionAsync();
            
            var product = new Product
            {
                Name = command.Name,
                Description = command.Description,
                Price = command.Price,
                CategoryId = command.CategoryId,
                IsActive = true,
                CreatedAt = DateTime.UtcNow
            };
            
            var createdProduct = await _unitOfWork.Products.AddAsync(product);
            await _unitOfWork.SaveChangesAsync();
            await _unitOfWork.CommitTransactionAsync();
            
            _logger.LogInformation("Product created successfully: {ProductId}", createdProduct.Id);
            
            return new CreateProductResult
            {
                Success = true,
                ProductId = createdProduct.Id,
                Message = "Product created successfully"
            };
        }
        catch (Exception ex)
        {
            await _unitOfWork.RollbackTransactionAsync();
            _logger.LogError(ex, "Error creating product");
            
            return new CreateProductResult
            {
                Success = false,
                Message = "Failed to create product"
            };
        }
    }
}

// Example Queries
public class GetProductByIdQuery : IQuery<ProductDto>
{
    public int ProductId { get; set; }
}

public class GetProductByIdQueryHandler : IQueryHandler<GetProductByIdQuery, ProductDto>
{
    private readonly IProductQueryRepository _queryRepository;
    private readonly ICacheService _cacheService;
    
    public async Task<ProductDto> HandleAsync(GetProductByIdQuery query)
    {
        var cacheKey = $"product:{query.ProductId}";
        var cachedProduct = await _cacheService.GetAsync<ProductDto>(cacheKey);
        
        if (cachedProduct != null)
        {
            return cachedProduct;
        }
        
        var product = await _queryRepository.GetProductByIdAsync(query.ProductId);
        
        if (product != null)
        {
            await _cacheService.SetAsync(cacheKey, product, TimeSpan.FromMinutes(15));
        }
        
        return product;
    }
}
```

### Caching Strategy Implementation

#### 1. Multi-Level Caching
```csharp
public interface ICacheService
{
    Task<T> GetAsync<T>(string key) where T : class;
    Task SetAsync<T>(string key, T value, TimeSpan? expiration = null) where T : class;
    Task RemoveAsync(string key);
    Task RemovePatternAsync(string pattern);
    Task<bool> ExistsAsync(string key);
}

public class MultiLevelCacheService : ICacheService
{
    private readonly IMemoryCache _memoryCache;
    private readonly IDistributedCache _distributedCache;
    private readonly ILogger<MultiLevelCacheService> _logger;
    
    public MultiLevelCacheService(
        IMemoryCache memoryCache,
        IDistributedCache distributedCache,
        ILogger<MultiLevelCacheService> logger)
    {
        _memoryCache = memoryCache;
        _distributedCache = distributedCache;
        _logger = logger;
    }
    
    public async Task<T> GetAsync<T>(string key) where T : class
    {
        // Try L1 cache (memory) first
        if (_memoryCache.TryGetValue(key, out T memoryValue))
        {
            _logger.LogDebug("Cache hit (L1): {Key}", key);
            return memoryValue;
        }
        
        // Try L2 cache (distributed)
        try
        {
            var distributedValue = await _distributedCache.GetStringAsync(key);
            if (distributedValue != null)
            {
                var value = JsonSerializer.Deserialize<T>(distributedValue);
                
                // Store in L1 cache for faster subsequent access
                _memoryCache.Set(key, value, TimeSpan.FromMinutes(5));
                
                _logger.LogDebug("Cache hit (L2): {Key}", key);
                return value;
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Error accessing distributed cache for key: {Key}", key);
        }
        
        _logger.LogDebug("Cache miss: {Key}", key);
        return null;
    }
    
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiration = null) where T : class
    {
        var cacheExpiration = expiration ?? TimeSpan.FromMinutes(30);
        
        // Set in L1 cache (memory)
        _memoryCache.Set(key, value, TimeSpan.FromMinutes(Math.Min(5, cacheExpiration.TotalMinutes)));
        
        // Set in L2 cache (distributed)
        try
        {
            var serializedValue = JsonSerializer.Serialize(value);
            var options = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = cacheExpiration
            };
            
            await _distributedCache.SetStringAsync(key, serializedValue, options);
            
            _logger.LogDebug("Cache set: {Key}", key);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Error setting distributed cache for key: {Key}", key);
        }
    }
    
    public async Task RemoveAsync(string key)
    {
        // Remove from L1 cache
        _memoryCache.Remove(key);
        
        // Remove from L2 cache
        try
        {
            await _distributedCache.RemoveAsync(key);
            _logger.LogDebug("Cache removed: {Key}", key);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Error removing from distributed cache for key: {Key}", key);
        }
    }
    
    public async Task RemovePatternAsync(string pattern)
    {
        // This is a simplified implementation
        // In production, you might need a more sophisticated pattern matching
        // or use Redis-specific commands for pattern-based removal
        
        _logger.LogWarning("Pattern-based cache removal not fully implemented: {Pattern}", pattern);
        
        // For Redis, you could use:
        // var server = _redis.GetServer(endpoint);
        // var keys = server.Keys(pattern: pattern);
        // await _distributedCache.RemoveAsync(keys);
    }
    
    public async Task<bool> ExistsAsync(string key)
    {
        // Check L1 cache
        if (_memoryCache.TryGetValue(key, out _))
        {
            return true;
        }
        
        // Check L2 cache
        try
        {
            var value = await _distributedCache.GetStringAsync(key);
            return value != null;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Error checking cache existence for key: {Key}", key);
            return false;
        }
    }
}
```

### Connection Pool and Performance Optimization

#### 1. Connection Pool Management
```csharp
public class OptimizedDbContext : DbContext
{
    public OptimizedDbContext(DbContextOptions<OptimizedDbContext> options) : base(options) { }
    
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseSqlServer(connectionString, options =>
            {
                // Enable connection pooling
                options.EnableRetryOnFailure(
                    maxRetryCount: 3,
                    maxRetryDelay: TimeSpan.FromSeconds(30),
                    errorNumbersToAdd: null);
                
                // Configure command timeout
                options.CommandTimeout(30);
            });
            
            // Enable sensitive data logging in development only
            #if DEBUG
            optionsBuilder.EnableSensitiveDataLogging();
            optionsBuilder.EnableDetailedErrors();
            #endif
            
            // Configure query behavior
            optionsBuilder.ConfigureWarnings(warnings =>
            {
                warnings.Throw(RelationalEventId.QueryClientEvaluationWarning);
            });
        }
        
        base.OnConfiguring(optionsBuilder);
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure global query filters
        modelBuilder.Entity<Product>().HasQueryFilter(p => p.IsActive);
        
        // Configure indexes for performance
        modelBuilder.Entity<Product>()
            .HasIndex(p => new { p.CategoryId, p.IsActive })
            .HasDatabaseName("IX_Product_CategoryId_IsActive");
        
        modelBuilder.Entity<Product>()
            .HasIndex(p => p.Name)
            .HasDatabaseName("IX_Product_Name");
        
        base.OnModelCreating(modelBuilder);
    }
}

// Connection monitoring and health checks
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly IDbConnectionFactory _connectionFactory;
    
    public DatabaseHealthCheck(IDbConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var connection = await _connectionFactory.CreateConnectionAsync();
            
            var command = connection.CreateCommand();
            command.CommandText = "SELECT 1";
            
            var result = await command.ExecuteScalarAsync(cancellationToken);
            
            if (result?.ToString() == "1")
            {
                return HealthCheckResult.Healthy("Database connection is healthy");
            }
            
            return HealthCheckResult.Unhealthy("Database returned unexpected result");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Database connection failed", ex);
        }
    }
}
```

## WebForms Integration Examples

### Modernized WebForms Page with New Data Access
```csharp
// Product management page with modern data access
public partial class ProductManagement : Page
{
    private readonly IMediator _mediator;
    private readonly ILogger<ProductManagement> _logger;
    
    // Dependency injection in WebForms (using custom page factory)
    public ProductManagement(IMediator mediator, ILogger<ProductManagement> logger)
    {
        _mediator = mediator;
        _logger = logger;
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadProductsAsync();
            await LoadCategoriesAsync();
        }
    }
    
    private async Task LoadProductsAsync()
    {
        try
        {
            var query = new GetProductsPagedQuery
            {
                PageIndex = GetCurrentPage(),
                PageSize = GetPageSize(),
                SortColumn = GetSortColumn(),
                SortAscending = GetSortAscending()
            };
            
            var result = await _mediator.SendAsync(query);
            
            GridView1.DataSource = result.Items;
            GridView1.VirtualItemCount = result.TotalCount;
            GridView1.DataBind();
            
            UpdatePagingControls(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error loading products");
            ShowErrorMessage("Failed to load products");
        }
    }
    
    private async Task LoadCategoriesAsync()
    {
        try
        {
            var query = new GetAllCategoriesQuery();
            var categories = await _mediator.SendAsync(query);
            
            ddlCategory.Items.Clear();
            ddlCategory.Items.Add(new ListItem("All Categories", ""));
            
            foreach (var category in categories)
            {
                ddlCategory.Items.Add(new ListItem(category.Name, category.Id.ToString()));
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error loading categories");
            ShowErrorMessage("Failed to load categories");
        }
    }
    
    protected async void btnCreate_Click(object sender, EventArgs e)
    {
        if (Page.IsValid)
        {
            try
            {
                var command = new CreateProductCommand
                {
                    Name = txtName.Text,
                    Description = txtDescription.Text,
                    Price = decimal.Parse(txtPrice.Text),
                    CategoryId = int.Parse(ddlCategory.SelectedValue)
                };
                
                var result = await _mediator.SendAsync(command);
                
                if (result.Success)
                {
                    ShowSuccessMessage("Product created successfully");
                    ClearForm();
                    await LoadProductsAsync();
                }
                else
                {
                    ShowErrorMessage(result.Message);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating product");
                ShowErrorMessage("Failed to create product");
            }
        }
    }
    
    protected async void GridView1_RowDeleting(object sender, GridViewDeleteEventArgs e)
    {
        try
        {
            var productId = Convert.ToInt32(GridView1.DataKeys[e.RowIndex].Value);
            
            var command = new DeleteProductCommand { ProductId = productId };
            var result = await _mediator.SendAsync(command);
            
            if (result.Success)
            {
                ShowSuccessMessage("Product deleted successfully");
                await LoadProductsAsync();
            }
            else
            {
                ShowErrorMessage(result.Message);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error deleting product");
            ShowErrorMessage("Failed to delete product");
        }
    }
    
    protected async void GridView1_PageIndexChanging(object sender, GridViewPageEventArgs e)
    {
        GridView1.PageIndex = e.NewPageIndex;
        await LoadProductsAsync();
    }
    
    protected async void GridView1_Sorting(object sender, GridViewSortEventArgs e)
    {
        // Handle sorting logic
        UpdateSortingState(e.SortExpression, e.SortDirection);
        await LoadProductsAsync();
    }
    
    // Helper methods
    private int GetCurrentPage() => GridView1.PageIndex;
    private int GetPageSize() => GridView1.PageSize;
    private string GetSortColumn() => ViewState["SortColumn"]?.ToString() ?? "Name";
    private bool GetSortAscending() => ViewState["SortAscending"] as bool? ?? true;
    
    private void UpdateSortingState(string sortExpression, SortDirection sortDirection)
    {
        ViewState["SortColumn"] = sortExpression;
        ViewState["SortAscending"] = sortDirection == SortDirection.Ascending;
    }
    
    private void ShowSuccessMessage(string message)
    {
        lblSuccess.Text = message;
        lblSuccess.Visible = true;
        lblError.Visible = false;
    }
    
    private void ShowErrorMessage(string message)
    {
        lblError.Text = message;
        lblError.Visible = true;
        lblSuccess.Visible = false;
    }
    
    private void ClearForm()
    {
        txtName.Text = "";
        txtDescription.Text = "";
        txtPrice.Text = "";
        ddlCategory.SelectedIndex = 0;
    }
    
    private void UpdatePagingControls(PagedResult<ProductDto> result)
    {
        // Update paging UI controls
        lblPageInfo.Text = $"Page {result.PageIndex + 1} of {result.TotalPages} ({result.TotalCount} total items)";
    }
}
```

## Migration Timeline and Strategy

### Phase 1: Foundation (4-6 weeks)
1. **Infrastructure Setup**
   - Set up EF Core or Dapper
   - Configure dependency injection
   - Implement base repository patterns

2. **Core Services**
   - Create base service interfaces
   - Implement logging and caching
   - Set up health checks

### Phase 2: Data Layer Migration (6-8 weeks)
1. **Repository Implementation**
   - Create specific repositories
   - Implement Unit of Work pattern
   - Add validation and error handling

2. **Service Layer Development**
   - Business logic services
   - CQRS implementation (if applicable)
   - Integration testing

### Phase 3: Page Integration (8-12 weeks)
1. **WebForms Integration**
   - Update pages to use new data access
   - Implement async patterns
   - Add caching strategies

2. **Performance Optimization**
   - Connection pool tuning
   - Query optimization
   - Caching refinement

### Phase 4: Testing and Deployment (2-4 weeks)
1. **Comprehensive Testing**
   - Unit tests for repositories and services
   - Integration tests for data access
   - Performance testing

2. **Production Deployment**
   - Database migration scripts
   - Connection string updates
   - Monitoring implementation

## Success Metrics

### Performance Metrics
- **Query Performance**: 50%+ improvement in query execution time
- **Connection Efficiency**: Reduced connection pool usage
- **Memory Usage**: 30%+ reduction in memory footprint

### Code Quality Metrics
- **Testability**: 80%+ code coverage
- **Maintainability**: Reduced cyclomatic complexity
- **Separation of Concerns**: Clear layer boundaries

### Business Metrics
- **Development Velocity**: 40%+ faster feature development
- **Bug Reduction**: 60%+ fewer data-related bugs
- **Scalability**: Support for 10x user load

## Conclusion

Modernizing the data access layer is crucial for WebForms migration success. The key strategies are:

1. **Repository Pattern**: Abstract data access for testability
2. **Service Layer**: Implement business logic separation
3. **Caching Strategy**: Multi-level caching for performance
4. **CQRS**: Separate read and write operations for scalability
5. **Performance Optimization**: Connection pooling and query optimization
6. **Testing**: Comprehensive unit and integration testing

This modernization provides a solid foundation for eventual migration to modern frameworks while immediately improving code quality, performance, and maintainability.