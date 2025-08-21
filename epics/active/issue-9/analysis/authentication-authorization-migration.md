# Authentication and Authorization Migration Guide

## Overview

Authentication and authorization systems in legacy WebForms applications often rely on outdated patterns and technologies. This guide provides comprehensive strategies for migrating to modern identity and access management systems while maintaining security and functionality.

## Legacy Authentication Analysis

### Common WebForms Authentication Patterns

#### 1. Forms Authentication with Membership Provider
```csharp
// Legacy web.config authentication
<system.web>
    <authentication mode="Forms">
        <forms loginUrl="~/Login.aspx" 
               protection="All" 
               timeout="30" 
               name=".ASPXAUTH"
               path="/" 
               requireSSL="false" 
               slidingExpiration="true"
               defaultUrl="~/Default.aspx" />
    </authentication>
    
    <membership defaultProvider="SqlServerMembershipProvider">
        <providers>
            <add name="SqlServerMembershipProvider"
                 type="System.Web.Security.SqlMembershipProvider"
                 connectionStringName="MembershipConnection"
                 applicationName="/MyApp"
                 minRequiredPasswordLength="8"
                 minRequiredNonalphanumericCharacters="1"
                 passwordStrengthRegularExpression=""
                 enablePasswordRetrieval="false"
                 enablePasswordReset="true"
                 requiresQuestionAndAnswer="false"
                 requiresUniqueEmail="true"
                 passwordFormat="Hashed" />
        </providers>
    </membership>
    
    <roleManager enabled="true" defaultProvider="SqlServerRoleProvider">
        <providers>
            <add name="SqlServerRoleProvider"
                 type="System.Web.Security.SqlRoleProvider"
                 connectionStringName="MembershipConnection"
                 applicationName="/MyApp" />
        </providers>
    </roleManager>
</system.web>

// Legacy login page
public partial class Login : Page
{
    protected void btnLogin_Click(object sender, EventArgs e)
    {
        if (Membership.ValidateUser(txtUsername.Text, txtPassword.Text))
        {
            FormsAuthentication.SetAuthCookie(txtUsername.Text, chkRememberMe.Checked);
            
            string returnUrl = Request.QueryString["ReturnUrl"];
            if (string.IsNullOrEmpty(returnUrl))
            {
                Response.Redirect("~/Default.aspx");
            }
            else
            {
                Response.Redirect(returnUrl);
            }
        }
        else
        {
            lblError.Text = "Invalid username or password";
        }
    }
}

// Legacy authorization in pages
public partial class AdminPanel : Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!User.Identity.IsAuthenticated)
        {
            Response.Redirect("~/Login.aspx");
            return;
        }
        
        if (!Roles.IsUserInRole("Administrator"))
        {
            Response.Redirect("~/AccessDenied.aspx");
            return;
        }
    }
}
```

#### 2. Custom Authentication Implementation
```csharp
// Legacy custom authentication
public class CustomAuthenticationModule : IHttpModule
{
    public void Init(HttpApplication context)
    {
        context.AuthenticateRequest += Context_AuthenticateRequest;
        context.PostAuthenticateRequest += Context_PostAuthenticateRequest;
    }
    
    private void Context_AuthenticateRequest(object sender, EventArgs e)
    {
        var context = HttpContext.Current;
        var authCookie = context.Request.Cookies["CustomAuth"];
        
        if (authCookie != null)
        {
            try
            {
                var ticket = FormsAuthentication.Decrypt(authCookie.Value);
                if (ticket != null && !ticket.Expired)
                {
                    var identity = new GenericIdentity(ticket.Name);
                    var principal = new GenericPrincipal(identity, GetUserRoles(ticket.Name));
                    context.User = principal;
                }
            }
            catch
            {
                // Invalid ticket
                context.Response.Cookies.Remove("CustomAuth");
            }
        }
    }
    
    private string[] GetUserRoles(string username)
    {
        // Database lookup for roles
        using (var connection = new SqlConnection(ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString))
        {
            connection.Open();
            var command = new SqlCommand(@"
                SELECT r.RoleName 
                FROM Users u
                INNER JOIN UserRoles ur ON u.UserId = ur.UserId
                INNER JOIN Roles r ON ur.RoleId = r.RoleId
                WHERE u.Username = @Username", connection);
            
            command.Parameters.AddWithValue("@Username", username);
            var reader = command.ExecuteReader();
            
            var roles = new List<string>();
            while (reader.Read())
            {
                roles.Add(reader["RoleName"].ToString());
            }
            
            return roles.ToArray();
        }
    }
}
```

## Modern Identity Architecture

### ASP.NET Core Identity Implementation

#### 1. Identity Models and Configuration
```csharp
// Modern user entity
public class ApplicationUser : IdentityUser<int>
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? LastLoginAt { get; set; }
    public bool IsActive { get; set; }
    public string RefreshToken { get; set; }
    public DateTime? RefreshTokenExpiryTime { get; set; }
    
    // Navigation properties
    public virtual ICollection<ApplicationUserRole> UserRoles { get; set; }
    public virtual ICollection<ApplicationUserClaim> UserClaims { get; set; }
    public virtual ICollection<UserLoginHistory> LoginHistory { get; set; }
}

public class ApplicationRole : IdentityRole<int>
{
    public string Description { get; set; }
    public DateTime CreatedAt { get; set; }
    public bool IsActive { get; set; }
    
    // Navigation properties
    public virtual ICollection<ApplicationUserRole> UserRoles { get; set; }
    public virtual ICollection<ApplicationRoleClaim> RoleClaims { get; set; }
}

public class ApplicationUserRole : IdentityUserRole<int>
{
    public virtual ApplicationUser User { get; set; }
    public virtual ApplicationRole Role { get; set; }
    public DateTime AssignedAt { get; set; }
    public string AssignedBy { get; set; }
}

public class ApplicationUserClaim : IdentityUserClaim<int>
{
    public virtual ApplicationUser User { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class ApplicationRoleClaim : IdentityRoleClaim<int>
{
    public virtual ApplicationRole Role { get; set; }
    public DateTime CreatedAt { get; set; }
}

// DbContext configuration
public class ApplicationIdentityDbContext : IdentityDbContext<
    ApplicationUser, 
    ApplicationRole, 
    int,
    ApplicationUserClaim,
    ApplicationUserRole,
    IdentityUserLogin<int>,
    ApplicationRoleClaim,
    IdentityUserToken<int>>
{
    public ApplicationIdentityDbContext(DbContextOptions<ApplicationIdentityDbContext> options) : base(options) { }
    
    public DbSet<UserLoginHistory> UserLoginHistory { get; set; }
    
    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        
        // Configure Identity entities
        builder.Entity<ApplicationUser>(entity =>
        {
            entity.ToTable("Users");
            entity.Property(e => e.FirstName).HasMaxLength(100);
            entity.Property(e => e.LastName).HasMaxLength(100);
            entity.HasIndex(e => e.Email).IsUnique();
        });
        
        builder.Entity<ApplicationRole>(entity =>
        {
            entity.ToTable("Roles");
            entity.Property(e => e.Description).HasMaxLength(500);
            entity.HasIndex(e => e.Name).IsUnique();
        });
        
        builder.Entity<ApplicationUserRole>(entity =>
        {
            entity.ToTable("UserRoles");
            entity.HasKey(e => new { e.UserId, e.RoleId });
            
            entity.HasOne(e => e.User)
                  .WithMany(u => u.UserRoles)
                  .HasForeignKey(e => e.UserId);
                  
            entity.HasOne(e => e.Role)
                  .WithMany(r => r.UserRoles)
                  .HasForeignKey(e => e.RoleId);
        });
        
        builder.Entity<ApplicationUserClaim>(entity =>
        {
            entity.ToTable("UserClaims");
            entity.HasOne(e => e.User)
                  .WithMany(u => u.UserClaims)
                  .HasForeignKey(e => e.UserId);
        });
        
        builder.Entity<ApplicationRoleClaim>(entity =>
        {
            entity.ToTable("RoleClaims");
            entity.HasOne(e => e.Role)
                  .WithMany(r => r.RoleClaims)
                  .HasForeignKey(e => e.RoleId);
        });
        
        // Configure additional entities
        builder.Entity<UserLoginHistory>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.IpAddress).HasMaxLength(45);
            entity.Property(e => e.UserAgent).HasMaxLength(500);
            entity.HasIndex(e => new { e.UserId, e.LoginTime });
        });
    }
}

// Identity service configuration
public static class IdentityServiceExtensions
{
    public static IServiceCollection AddApplicationIdentity(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<ApplicationIdentityDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));
        
        services.AddIdentity<ApplicationUser, ApplicationRole>(options =>
        {
            // Password settings
            options.Password.RequireDigit = true;
            options.Password.RequiredLength = 8;
            options.Password.RequireNonAlphanumeric = true;
            options.Password.RequireUppercase = true;
            options.Password.RequireLowercase = true;
            options.Password.RequiredUniqueChars = 6;
            
            // Lockout settings
            options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(30);
            options.Lockout.MaxFailedAccessAttempts = 5;
            options.Lockout.AllowedForNewUsers = true;
            
            // User settings
            options.User.RequireUniqueEmail = true;
            options.User.AllowedUserNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@+";
            
            // Sign-in settings
            options.SignIn.RequireConfirmedEmail = true;
            options.SignIn.RequireConfirmedPhoneNumber = false;
        })
        .AddEntityFrameworkStores<ApplicationIdentityDbContext>()
        .AddDefaultTokenProviders();
        
        // Add custom services
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IRoleService, RoleService>();
        services.AddScoped<IAuthenticationService, AuthenticationService>();
        services.AddScoped<IAuthorizationService, AuthorizationService>();
        
        return services;
    }
}
```

#### 2. JWT Token Implementation
```csharp
public interface ITokenService
{
    Task<TokenResponse> GenerateTokenAsync(ApplicationUser user);
    Task<TokenResponse> RefreshTokenAsync(string refreshToken);
    ClaimsPrincipal GetPrincipalFromExpiredToken(string token);
    Task<bool> ValidateTokenAsync(string token);
    Task RevokeTokenAsync(string refreshToken);
}

public class JwtTokenService : ITokenService
{
    private readonly UserManager<ApplicationUser> _userManager;
    private readonly RoleManager<ApplicationRole> _roleManager;
    private readonly IConfiguration _configuration;
    private readonly ILogger<JwtTokenService> _logger;
    private readonly IUserService _userService;
    
    public JwtTokenService(
        UserManager<ApplicationUser> userManager,
        RoleManager<ApplicationRole> roleManager,
        IConfiguration configuration,
        ILogger<JwtTokenService> logger,
        IUserService userService)
    {
        _userManager = userManager;
        _roleManager = roleManager;
        _configuration = configuration;
        _logger = logger;
        _userService = userService;
    }
    
    public async Task<TokenResponse> GenerateTokenAsync(ApplicationUser user)
    {
        try
        {
            var claims = await GetClaimsAsync(user);
            
            var jwtSettings = _configuration.GetSection("JwtSettings");
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings["Secret"]));
            var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            
            var accessTokenExpiry = DateTime.UtcNow.AddMinutes(jwtSettings.GetValue<int>("AccessTokenExpirationMinutes"));
            var refreshTokenExpiry = DateTime.UtcNow.AddDays(jwtSettings.GetValue<int>("RefreshTokenExpirationDays"));
            
            var token = new JwtSecurityToken(
                issuer: jwtSettings["Issuer"],
                audience: jwtSettings["Audience"],
                claims: claims,
                expires: accessTokenExpiry,
                signingCredentials: credentials
            );
            
            var accessToken = new JwtSecurityTokenHandler().WriteToken(token);
            var refreshToken = GenerateRefreshToken();
            
            // Save refresh token to database
            user.RefreshToken = refreshToken;
            user.RefreshTokenExpiryTime = refreshTokenExpiry;
            user.LastLoginAt = DateTime.UtcNow;
            
            await _userManager.UpdateAsync(user);
            
            // Log login
            await _userService.LogUserLoginAsync(user.Id, GetClientIpAddress(), GetUserAgent());
            
            return new TokenResponse
            {
                AccessToken = accessToken,
                RefreshToken = refreshToken,
                AccessTokenExpiry = accessTokenExpiry,
                RefreshTokenExpiry = refreshTokenExpiry,
                TokenType = "Bearer"
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error generating token for user: {UserId}", user.Id);
            throw;
        }
    }
    
    public async Task<TokenResponse> RefreshTokenAsync(string refreshToken)
    {
        try
        {
            var user = await _userManager.Users
                .FirstOrDefaultAsync(u => u.RefreshToken == refreshToken && 
                                        u.RefreshTokenExpiryTime > DateTime.UtcNow);
            
            if (user == null)
            {
                throw new UnauthorizedAccessException("Invalid or expired refresh token");
            }
            
            return await GenerateTokenAsync(user);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error refreshing token");
            throw;
        }
    }
    
    public ClaimsPrincipal GetPrincipalFromExpiredToken(string token)
    {
        var jwtSettings = _configuration.GetSection("JwtSettings");
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtSettings["Secret"]));
        
        var tokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = false, // Don't validate lifetime for expired tokens
            ValidateIssuerSigningKey = true,
            ValidIssuer = jwtSettings["Issuer"],
            ValidAudience = jwtSettings["Audience"],
            IssuerSigningKey = key,
            ClockSkew = TimeSpan.Zero
        };
        
        var tokenHandler = new JwtSecurityTokenHandler();
        var principal = tokenHandler.ValidateToken(token, tokenValidationParameters, out var securityToken);
        
        if (!(securityToken is JwtSecurityToken jwtSecurityToken) ||
            !jwtSecurityToken.Header.Alg.Equals(SecurityAlgorithms.HmacSha256, StringComparison.InvariantCultureIgnoreCase))
        {
            throw new SecurityTokenException("Invalid token");
        }
        
        return principal;
    }
    
    public async Task<bool> ValidateTokenAsync(string token)
    {
        try
        {
            var principal = GetPrincipalFromExpiredToken(token);
            var userId = principal.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            
            if (string.IsNullOrEmpty(userId))
                return false;
            
            var user = await _userManager.FindByIdAsync(userId);
            return user != null && user.IsActive;
        }
        catch
        {
            return false;
        }
    }
    
    public async Task RevokeTokenAsync(string refreshToken)
    {
        try
        {
            var user = await _userManager.Users
                .FirstOrDefaultAsync(u => u.RefreshToken == refreshToken);
            
            if (user != null)
            {
                user.RefreshToken = null;
                user.RefreshTokenExpiryTime = null;
                await _userManager.UpdateAsync(user);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error revoking token");
            throw;
        }
    }
    
    private async Task<List<Claim>> GetClaimsAsync(ApplicationUser user)
    {
        var claims = new List<Claim>
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Name, user.UserName),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim("first_name", user.FirstName ?? ""),
            new Claim("last_name", user.LastName ?? ""),
            new Claim("is_active", user.IsActive.ToString()),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new Claim(JwtRegisteredClaimNames.Iat, new DateTimeOffset(DateTime.UtcNow).ToUnixTimeSeconds().ToString(), ClaimValueTypes.Integer64)
        };
        
        // Add roles
        var roles = await _userManager.GetRolesAsync(user);
        foreach (var role in roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role));
        }
        
        // Add custom claims
        var userClaims = await _userManager.GetClaimsAsync(user);
        claims.AddRange(userClaims);
        
        // Add role claims
        foreach (var roleName in roles)
        {
            var role = await _roleManager.FindByNameAsync(roleName);
            if (role != null)
            {
                var roleClaims = await _roleManager.GetClaimsAsync(role);
                claims.AddRange(roleClaims);
            }
        }
        
        return claims;
    }
    
    private string GenerateRefreshToken()
    {
        var randomBytes = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }
    
    private string GetClientIpAddress()
    {
        // Implementation to get client IP address
        return HttpContext.Current?.Request.UserHostAddress ?? "unknown";
    }
    
    private string GetUserAgent()
    {
        return HttpContext.Current?.Request.UserAgent ?? "unknown";
    }
}

// Token response model
public class TokenResponse
{
    public string AccessToken { get; set; }
    public string RefreshToken { get; set; }
    public DateTime AccessTokenExpiry { get; set; }
    public DateTime RefreshTokenExpiry { get; set; }
    public string TokenType { get; set; }
}
```

#### 3. Modern Authentication Service
```csharp
public interface IAuthenticationService
{
    Task<AuthenticationResult> LoginAsync(LoginRequest request);
    Task<AuthenticationResult> RegisterAsync(RegisterRequest request);
    Task<TokenResponse> RefreshTokenAsync(RefreshTokenRequest request);
    Task LogoutAsync(string refreshToken);
    Task<bool> ForgotPasswordAsync(ForgotPasswordRequest request);
    Task<bool> ResetPasswordAsync(ResetPasswordRequest request);
    Task<bool> ConfirmEmailAsync(ConfirmEmailRequest request);
    Task<bool> ChangePasswordAsync(string userId, ChangePasswordRequest request);
}

public class AuthenticationService : IAuthenticationService
{
    private readonly UserManager<ApplicationUser> _userManager;
    private readonly SignInManager<ApplicationUser> _signInManager;
    private readonly ITokenService _tokenService;
    private readonly IEmailService _emailService;
    private readonly ILogger<AuthenticationService> _logger;
    private readonly IConfiguration _configuration;
    
    public AuthenticationService(
        UserManager<ApplicationUser> userManager,
        SignInManager<ApplicationUser> signInManager,
        ITokenService tokenService,
        IEmailService emailService,
        ILogger<AuthenticationService> logger,
        IConfiguration configuration)
    {
        _userManager = userManager;
        _signInManager = signInManager;
        _tokenService = tokenService;
        _emailService = emailService;
        _logger = logger;
        _configuration = configuration;
    }
    
    public async Task<AuthenticationResult> LoginAsync(LoginRequest request)
    {
        try
        {
            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null)
            {
                return AuthenticationResult.Failed("Invalid email or password");
            }
            
            if (!user.IsActive)
            {
                return AuthenticationResult.Failed("Account is disabled");
            }
            
            if (!user.EmailConfirmed)
            {
                return AuthenticationResult.Failed("Email not confirmed");
            }
            
            var result = await _signInManager.CheckPasswordSignInAsync(user, request.Password, lockoutOnFailure: true);
            
            if (result.Succeeded)
            {
                var tokenResponse = await _tokenService.GenerateTokenAsync(user);
                
                _logger.LogInformation("User logged in successfully: {UserId}", user.Id);
                
                return AuthenticationResult.Success(tokenResponse, user);
            }
            
            if (result.IsLockedOut)
            {
                _logger.LogWarning("User account locked out: {UserId}", user.Id);
                return AuthenticationResult.Failed("Account locked out");
            }
            
            if (result.RequiresTwoFactor)
            {
                return AuthenticationResult.RequiresTwoFactor();
            }
            
            _logger.LogWarning("Failed login attempt for user: {Email}", request.Email);
            return AuthenticationResult.Failed("Invalid email or password");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during login for email: {Email}", request.Email);
            return AuthenticationResult.Failed("An error occurred during login");
        }
    }
    
    public async Task<AuthenticationResult> RegisterAsync(RegisterRequest request)
    {
        try
        {
            var existingUser = await _userManager.FindByEmailAsync(request.Email);
            if (existingUser != null)
            {
                return AuthenticationResult.Failed("Email already registered");
            }
            
            var user = new ApplicationUser
            {
                UserName = request.Email,
                Email = request.Email,
                FirstName = request.FirstName,
                LastName = request.LastName,
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            };
            
            var result = await _userManager.CreateAsync(user, request.Password);
            
            if (result.Succeeded)
            {
                // Add default role
                await _userManager.AddToRoleAsync(user, "User");
                
                // Send confirmation email
                var confirmationToken = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                await SendConfirmationEmailAsync(user, confirmationToken);
                
                _logger.LogInformation("User registered successfully: {UserId}", user.Id);
                
                return AuthenticationResult.Success(message: "Registration successful. Please check your email to confirm your account.");
            }
            
            var errors = string.Join("; ", result.Errors.Select(e => e.Description));
            return AuthenticationResult.Failed(errors);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during registration for email: {Email}", request.Email);
            return AuthenticationResult.Failed("An error occurred during registration");
        }
    }
    
    public async Task<TokenResponse> RefreshTokenAsync(RefreshTokenRequest request)
    {
        try
        {
            return await _tokenService.RefreshTokenAsync(request.RefreshToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error refreshing token");
            throw;
        }
    }
    
    public async Task LogoutAsync(string refreshToken)
    {
        try
        {
            await _tokenService.RevokeTokenAsync(refreshToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during logout");
            throw;
        }
    }
    
    public async Task<bool> ForgotPasswordAsync(ForgotPasswordRequest request)
    {
        try
        {
            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user == null || !user.EmailConfirmed)
            {
                // Don't reveal that the user does not exist or is not confirmed
                return true;
            }
            
            var resetToken = await _userManager.GeneratePasswordResetTokenAsync(user);
            await SendPasswordResetEmailAsync(user, resetToken);
            
            _logger.LogInformation("Password reset requested for user: {UserId}", user.Id);
            
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during password reset request for email: {Email}", request.Email);
            return false;
        }
    }
    
    private async Task SendConfirmationEmailAsync(ApplicationUser user, string token)
    {
        var confirmationUrl = $"{_configuration["ApplicationUrl"]}/confirm-email?userId={user.Id}&token={WebUtility.UrlEncode(token)}";
        
        var emailBody = $@"
            <h2>Confirm Your Email</h2>
            <p>Please confirm your account by clicking <a href='{confirmationUrl}'>here</a>.</p>
        ";
        
        await _emailService.SendEmailAsync(user.Email, "Confirm your email", emailBody);
    }
    
    private async Task SendPasswordResetEmailAsync(ApplicationUser user, string token)
    {
        var resetUrl = $"{_configuration["ApplicationUrl"]}/reset-password?userId={user.Id}&token={WebUtility.UrlEncode(token)}";
        
        var emailBody = $@"
            <h2>Reset Your Password</h2>
            <p>Please reset your password by clicking <a href='{resetUrl}'>here</a>.</p>
        ";
        
        await _emailService.SendEmailAsync(user.Email, "Reset your password", emailBody);
    }
}

// Authentication result classes
public class AuthenticationResult
{
    public bool IsSuccess { get; set; }
    public string Message { get; set; }
    public TokenResponse Token { get; set; }
    public ApplicationUser User { get; set; }
    public bool RequiresTwoFactor { get; set; }
    public List<string> Errors { get; set; } = new List<string>();
    
    public static AuthenticationResult Success(TokenResponse token = null, ApplicationUser user = null, string message = null)
    {
        return new AuthenticationResult
        {
            IsSuccess = true,
            Token = token,
            User = user,
            Message = message
        };
    }
    
    public static AuthenticationResult Failed(string message)
    {
        return new AuthenticationResult
        {
            IsSuccess = false,
            Message = message
        };
    }
    
    public static AuthenticationResult RequiresTwoFactor()
    {
        return new AuthenticationResult
        {
            IsSuccess = false,
            RequiresTwoFactor = true,
            Message = "Two-factor authentication required"
        };
    }
}
```

## Authorization Implementation

### 1. Policy-Based Authorization
```csharp
// Authorization policies configuration
public static class AuthorizationPolicies
{
    public const string RequireAdminRole = "RequireAdminRole";
    public const string RequireManagerRole = "RequireManagerRole";
    public const string RequireUserRole = "RequireUserRole";
    public const string RequireEmailConfirmed = "RequireEmailConfirmed";
    public const string RequireActiveUser = "RequireActiveUser";
    public const string ManageUsers = "ManageUsers";
    public const string ManageRoles = "ManageRoles";
    public const string ViewReports = "ViewReports";
    public const string EditContent = "EditContent";
    
    public static void ConfigurePolicies(AuthorizationOptions options)
    {
        // Role-based policies
        options.AddPolicy(RequireAdminRole, policy =>
            policy.RequireRole("Administrator"));
            
        options.AddPolicy(RequireManagerRole, policy =>
            policy.RequireRole("Administrator", "Manager"));
            
        options.AddPolicy(RequireUserRole, policy =>
            policy.RequireRole("Administrator", "Manager", "User"));
        
        // Claim-based policies
        options.AddPolicy(ManageUsers, policy =>
            policy.RequireClaim("permission", "manage_users"));
            
        options.AddPolicy(ManageRoles, policy =>
            policy.RequireClaim("permission", "manage_roles"));
            
        options.AddPolicy(ViewReports, policy =>
            policy.RequireClaim("permission", "view_reports"));
            
        options.AddPolicy(EditContent, policy =>
            policy.RequireClaim("permission", "edit_content"));
        
        // Custom requirement policies
        options.AddPolicy(RequireEmailConfirmed, policy =>
            policy.AddRequirements(new EmailConfirmedRequirement()));
            
        options.AddPolicy(RequireActiveUser, policy =>
            policy.AddRequirements(new ActiveUserRequirement()));
    }
}

// Custom authorization requirements
public class EmailConfirmedRequirement : IAuthorizationRequirement { }

public class ActiveUserRequirement : IAuthorizationRequirement { }

public class EmailConfirmedRequirementHandler : AuthorizationHandler<EmailConfirmedRequirement>
{
    private readonly UserManager<ApplicationUser> _userManager;
    
    public EmailConfirmedRequirementHandler(UserManager<ApplicationUser> userManager)
    {
        _userManager = userManager;
    }
    
    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        EmailConfirmedRequirement requirement)
    {
        if (context.User.Identity.IsAuthenticated)
        {
            var user = await _userManager.GetUserAsync(context.User);
            if (user?.EmailConfirmed == true)
            {
                context.Succeed(requirement);
            }
        }
    }
}

public class ActiveUserRequirementHandler : AuthorizationHandler<ActiveUserRequirement>
{
    private readonly UserManager<ApplicationUser> _userManager;
    
    public ActiveUserRequirementHandler(UserManager<ApplicationUser> userManager)
    {
        _userManager = userManager;
    }
    
    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        ActiveUserRequirement requirement)
    {
        if (context.User.Identity.IsAuthenticated)
        {
            var user = await _userManager.GetUserAsync(context.User);
            if (user?.IsActive == true)
            {
                context.Succeed(requirement);
            }
        }
    }
}
```

### 2. Resource-Based Authorization
```csharp
// Resource authorization operations
public static class Operations
{
    public static OperationAuthorizationRequirement Create = new() { Name = nameof(Create) };
    public static OperationAuthorizationRequirement Read = new() { Name = nameof(Read) };
    public static OperationAuthorizationRequirement Update = new() { Name = nameof(Update) };
    public static OperationAuthorizationRequirement Delete = new() { Name = nameof(Delete) };
}

// Resource authorization handler
public class DocumentAuthorizationHandler : AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    private readonly UserManager<ApplicationUser> _userManager;
    
    public DocumentAuthorizationHandler(UserManager<ApplicationUser> userManager)
    {
        _userManager = userManager;
    }
    
    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document document)
    {
        if (context.User == null || document == null)
        {
            return;
        }
        
        // Administrators can do anything
        if (context.User.IsInRole("Administrator"))
        {
            context.Succeed(requirement);
            return;
        }
        
        var userId = _userManager.GetUserId(context.User);
        
        // Document owner can perform all operations
        if (document.CreatedBy == userId)
        {
            context.Succeed(requirement);
            return;
        }
        
        // Managers can read and update documents
        if (context.User.IsInRole("Manager") && 
            (requirement.Name == Operations.Read.Name || requirement.Name == Operations.Update.Name))
        {
            context.Succeed(requirement);
            return;
        }
        
        // Regular users can only read public documents
        if (requirement.Name == Operations.Read.Name && document.IsPublic)
        {
            context.Succeed(requirement);
            return;
        }
    }
}

// Usage in service
public class DocumentService : IDocumentService
{
    private readonly IAuthorizationService _authorizationService;
    private readonly IDocumentRepository _documentRepository;
    
    public async Task<Document> GetDocumentAsync(int documentId, ClaimsPrincipal user)
    {
        var document = await _documentRepository.GetByIdAsync(documentId);
        if (document == null)
        {
            throw new NotFoundException("Document not found");
        }
        
        var authResult = await _authorizationService.AuthorizeAsync(user, document, Operations.Read);
        if (!authResult.Succeeded)
        {
            throw new UnauthorizedAccessException("Access denied");
        }
        
        return document;
    }
    
    public async Task<Document> UpdateDocumentAsync(int documentId, UpdateDocumentRequest request, ClaimsPrincipal user)
    {
        var document = await _documentRepository.GetByIdAsync(documentId);
        if (document == null)
        {
            throw new NotFoundException("Document not found");
        }
        
        var authResult = await _authorizationService.AuthorizeAsync(user, document, Operations.Update);
        if (!authResult.Succeeded)
        {
            throw new UnauthorizedAccessException("Access denied");
        }
        
        // Update document
        document.Title = request.Title;
        document.Content = request.Content;
        document.UpdatedAt = DateTime.UtcNow;
        
        await _documentRepository.UpdateAsync(document);
        
        return document;
    }
}
```

## WebForms Integration with Modern Auth

### 1. Hybrid Authentication Bridge
```csharp
// Authentication bridge for WebForms
public class WebFormsAuthenticationBridge : IHttpModule
{
    private readonly IServiceProvider _serviceProvider;
    
    public void Init(HttpApplication context)
    {
        _serviceProvider = GetServiceProvider(); // Implementation to get DI container
        
        context.PostAuthenticateRequest += Context_PostAuthenticateRequest;
    }
    
    private void Context_PostAuthenticateRequest(object sender, EventArgs e)
    {
        var context = HttpContext.Current;
        
        // Check for JWT token in Authorization header
        var authHeader = context.Request.Headers["Authorization"];
        if (!string.IsNullOrEmpty(authHeader) && authHeader.StartsWith("Bearer "))
        {
            var token = authHeader.Substring("Bearer ".Length).Trim();
            
            var tokenService = _serviceProvider.GetService<ITokenService>();
            if (tokenService.ValidateTokenAsync(token).Result)
            {
                var principal = tokenService.GetPrincipalFromExpiredToken(token);
                context.User = principal;
                Thread.CurrentPrincipal = principal;
                return;
            }
        }
        
        // Check for JWT token in cookie (for WebForms pages)
        var jwtCookie = context.Request.Cookies["jwt_token"];
        if (jwtCookie != null && !string.IsNullOrEmpty(jwtCookie.Value))
        {
            var tokenService = _serviceProvider.GetService<ITokenService>();
            if (tokenService.ValidateTokenAsync(jwtCookie.Value).Result)
            {
                var principal = tokenService.GetPrincipalFromExpiredToken(jwtCookie.Value);
                context.User = principal;
                Thread.CurrentPrincipal = principal;
                return;
            }
        }
        
        // Fall back to Forms Authentication for legacy support
        if (context.User?.Identity?.IsAuthenticated == true)
        {
            // Convert FormsIdentity to ClaimsIdentity
            var formsIdentity = (FormsIdentity)context.User.Identity;
            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.Name, formsIdentity.Name),
                new Claim(ClaimTypes.NameIdentifier, formsIdentity.Name)
            };
            
            // Add roles from legacy provider
            var roles = Roles.GetRolesForUser(formsIdentity.Name);
            foreach (var role in roles)
            {
                claims.Add(new Claim(ClaimTypes.Role, role));
            }
            
            var claimsIdentity = new ClaimsIdentity(claims, "Forms");
            var claimsPrincipal = new ClaimsPrincipal(claimsIdentity);
            
            context.User = claimsPrincipal;
            Thread.CurrentPrincipal = claimsPrincipal;
        }
    }
}

// Base page with modern authentication
public abstract class AuthenticatedBasePage : Page
{
    protected IAuthorizationService AuthorizationService { get; private set; }
    protected UserManager<ApplicationUser> UserManager { get; private set; }
    protected ApplicationUser CurrentUser { get; private set; }
    
    protected override void OnInit(EventArgs e)
    {
        AuthorizationService = DependencyResolver.Current.GetService<IAuthorizationService>();
        UserManager = DependencyResolver.Current.GetService<UserManager<ApplicationUser>>();
        
        base.OnInit(e);
    }
    
    protected override async void OnLoad(EventArgs e)
    {
        if (!User.Identity.IsAuthenticated)
        {
            RedirectToLogin();
            return;
        }
        
        CurrentUser = await UserManager.GetUserAsync(User);
        if (CurrentUser == null || !CurrentUser.IsActive)
        {
            RedirectToLogin();
            return;
        }
        
        await CheckPageAuthorizationAsync();
        
        base.OnLoad(e);
    }
    
    protected virtual async Task CheckPageAuthorizationAsync()
    {
        // Override in derived pages to implement specific authorization logic
    }
    
    protected async Task<bool> IsAuthorizedAsync(string policy)
    {
        var result = await AuthorizationService.AuthorizeAsync(User, policy);
        return result.Succeeded;
    }
    
    protected async Task<bool> IsAuthorizedAsync<T>(T resource, OperationAuthorizationRequirement operation)
    {
        var result = await AuthorizationService.AuthorizeAsync(User, resource, operation);
        return result.Succeeded;
    }
    
    protected void RequireAuthorization(string policy)
    {
        if (!IsAuthorizedAsync(policy).Result)
        {
            RedirectToAccessDenied();
        }
    }
    
    private void RedirectToLogin()
    {
        var returnUrl = Request.RawUrl;
        Response.Redirect($"~/Login.aspx?ReturnUrl={HttpUtility.UrlEncode(returnUrl)}");
    }
    
    private void RedirectToAccessDenied()
    {
        Response.Redirect("~/AccessDenied.aspx");
    }
}

// Admin page example
public partial class AdminUsers : AuthenticatedBasePage
{
    protected override async Task CheckPageAuthorizationAsync()
    {
        RequireAuthorization(AuthorizationPolicies.RequireAdminRole);
    }
    
    protected async void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            await LoadUsersAsync();
        }
    }
    
    private async Task LoadUsersAsync()
    {
        var userService = DependencyResolver.Current.GetService<IUserService>();
        var users = await userService.GetUsersAsync();
        
        GridView1.DataSource = users;
        GridView1.DataBind();
    }
    
    protected async void GridView1_RowCommand(object sender, GridViewCommandEventArgs e)
    {
        if (e.CommandName == "ToggleStatus")
        {
            var userId = Convert.ToInt32(e.CommandArgument);
            var userService = DependencyResolver.Current.GetService<IUserService>();
            
            await userService.ToggleUserStatusAsync(userId);
            await LoadUsersAsync();
        }
    }
}
```

### 2. Modern Login Page Implementation
```csharp
// Modern login page with JWT support
public partial class Login : Page
{
    private readonly IAuthenticationService _authenticationService;
    private readonly ILogger<Login> _logger;
    
    public Login(IAuthenticationService authenticationService, ILogger<Login> logger)
    {
        _authenticationService = authenticationService;
        _logger = logger;
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        if (User.Identity.IsAuthenticated)
        {
            RedirectToReturnUrl();
        }
    }
    
    protected async void btnLogin_Click(object sender, EventArgs e)
    {
        if (!Page.IsValid)
            return;
        
        try
        {
            var loginRequest = new LoginRequest
            {
                Email = txtEmail.Text,
                Password = txtPassword.Text,
                RememberMe = chkRememberMe.Checked
            };
            
            var result = await _authenticationService.LoginAsync(loginRequest);
            
            if (result.IsSuccess)
            {
                // Set JWT token in cookie for WebForms compatibility
                var cookie = new HttpCookie("jwt_token", result.Token.AccessToken)
                {
                    HttpOnly = true,
                    Secure = Request.IsSecureConnection,
                    SameSite = SameSiteMode.Strict,
                    Expires = result.Token.AccessTokenExpiry
                };
                
                Response.Cookies.Add(cookie);
                
                // Set refresh token cookie
                var refreshCookie = new HttpCookie("refresh_token", result.Token.RefreshToken)
                {
                    HttpOnly = true,
                    Secure = Request.IsSecureConnection,
                    SameSite = SameSiteMode.Strict,
                    Expires = result.Token.RefreshTokenExpiry
                };
                
                Response.Cookies.Add(refreshCookie);
                
                _logger.LogInformation("User logged in successfully: {Email}", txtEmail.Text);
                
                RedirectToReturnUrl();
            }
            else if (result.RequiresTwoFactor)
            {
                Response.Redirect("~/TwoFactorAuth.aspx");
            }
            else
            {
                lblError.Text = result.Message;
                lblError.Visible = true;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during login attempt for email: {Email}", txtEmail.Text);
            lblError.Text = "An error occurred during login. Please try again.";
            lblError.Visible = true;
        }
    }
    
    private void RedirectToReturnUrl()
    {
        var returnUrl = Request.QueryString["ReturnUrl"];
        
        if (!string.IsNullOrEmpty(returnUrl) && IsLocalUrl(returnUrl))
        {
            Response.Redirect(returnUrl);
        }
        else
        {
            Response.Redirect("~/Default.aspx");
        }
    }
    
    private bool IsLocalUrl(string url)
    {
        if (string.IsNullOrEmpty(url))
            return false;
        
        return Uri.IsWellFormedUriString(url, UriKind.Relative) ||
               (Uri.IsWellFormedUriString(url, UriKind.Absolute) &&
                Uri.TryCreate(url, UriKind.Absolute, out var uri) &&
                string.Equals(uri.Host, Request.Url.Host, StringComparison.OrdinalIgnoreCase));
    }
}
```

## Migration Timeline and Strategy

### Phase 1: Infrastructure Setup (4-6 weeks)
1. **Identity Infrastructure**
   - Set up ASP.NET Core Identity
   - Configure JWT authentication
   - Create user and role models

2. **Database Migration**
   - Create new identity tables
   - Migrate existing users and roles
   - Preserve existing passwords (if possible)

### Phase 2: Authentication Services (6-8 weeks)
1. **Service Implementation**
   - Authentication service
   - Authorization service
   - Token service

2. **Integration Layer**
   - WebForms authentication bridge
   - API authentication middleware

### Phase 3: Page Migration (8-12 weeks)
1. **Base Page Classes**
   - Authenticated base page
   - Role-specific base pages
   - Authorization helpers

2. **Page-by-Page Migration**
   - Update login/logout pages
   - Migrate admin pages
   - Update user management

### Phase 4: Testing and Deployment (4-6 weeks)
1. **Security Testing**
   - Authentication testing
   - Authorization testing
   - Penetration testing

2. **Performance Testing**
   - Token generation/validation
   - Database query optimization
   - Load testing

## Success Metrics

### Security Metrics
- **Authentication Success Rate**: >99.9%
- **Token Security**: No token-related vulnerabilities
- **Session Management**: Secure session handling

### Performance Metrics
- **Login Performance**: <500ms authentication time
- **Token Validation**: <100ms validation time
- **Database Efficiency**: Optimized user/role queries

### Migration Metrics
- **User Migration**: 100% user data preservation
- **Functionality**: No loss of existing features
- **Security Enhancement**: Improved security posture

## Conclusion

Authentication and authorization migration is critical for WebForms modernization. Key strategies include:

1. **Modern Identity Framework**: ASP.NET Core Identity with JWT
2. **Policy-Based Authorization**: Flexible, maintainable authorization
3. **Hybrid Authentication**: Support both legacy and modern auth
4. **Security Enhancement**: Improved security practices
5. **Gradual Migration**: Maintain functionality during transition
6. **Comprehensive Testing**: Ensure security and performance

This approach provides a secure, scalable, and maintainable authentication system that supports both current WebForms applications and future modern frameworks.