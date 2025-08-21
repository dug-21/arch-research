# ASP.NET WebForms Master Pages Implementation Patterns

**Code Archaeologist Analysis**  
**Date**: August 15, 2025  
**Task**: Master Page Patterns and Implementation Examples  
**Coordination**: Hive Mind Architecture Analysis  

---

## Executive Summary

This document provides comprehensive examples of ASP.NET WebForms Master Pages implementation patterns, including hierarchical master pages, dynamic master page selection, and migration strategies.

## 1. Basic Master Page Implementation

### 1.1 Site Master Page (Site.Master)

```aspx
<%@ Master Language="C#" AutoEventWireup="true" CodeBehind="Site.master.cs" Inherits="WebFormsApp.SiteMaster" %>

<!DOCTYPE html>
<html lang="en">
<head runat="server">
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title><%: Page.Title %> - Enterprise Application</title>
    
    <!-- Meta tags from content pages -->
    <asp:ContentPlaceHolder ID="MetaContent" runat="server"></asp:ContentPlaceHolder>
    
    <!-- CSS References -->
    <asp:PlaceHolder runat="server">
        <%: System.Web.Optimization.Styles.Render("~/Content/css") %>
    </asp:PlaceHolder>
    <link href="~/favicon.ico" rel="shortcut icon" type="image/x-icon" />
    
    <!-- Additional CSS from content pages -->
    <asp:ContentPlaceHolder ID="CssContent" runat="server"></asp:ContentPlaceHolder>
</head>

<body>
    <form runat="server">
        <asp:ScriptManager runat="server" EnablePartialRendering="true">
            <Scripts>
                <%: System.Web.Optimization.Scripts.Render("~/bundles/modernizr") %>
            </Scripts>
        </asp:ScriptManager>

        <!-- Navigation Header -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <asp:LinkButton ID="lnkHome" runat="server" 
                    CssClass="navbar-brand" 
                    PostBackUrl="~/Default.aspx">
                    <img src="~/Images/logo.png" alt="Company Logo" height="30" />
                    Enterprise App
                </asp:LinkButton>
                
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarNav">
                    <!-- Main Navigation -->
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item">
                            <asp:HyperLink ID="lnkCustomers" runat="server" 
                                NavigateUrl="~/Customers/CustomerList.aspx" 
                                CssClass="nav-link">
                                Customers
                            </asp:HyperLink>
                        </li>
                        <li class="nav-item">
                            <asp:HyperLink ID="lnkOrders" runat="server" 
                                NavigateUrl="~/Orders/OrderList.aspx" 
                                CssClass="nav-link">
                                Orders
                            </asp:HyperLink>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="reportsDropdown" 
                               role="button" data-toggle="dropdown">
                                Reports
                            </a>
                            <div class="dropdown-menu">
                                <asp:HyperLink ID="lnkSalesReport" runat="server" 
                                    NavigateUrl="~/Reports/SalesReport.aspx" 
                                    CssClass="dropdown-item">
                                    Sales Report
                                </asp:HyperLink>
                                <asp:HyperLink ID="lnkCustomerReport" runat="server" 
                                    NavigateUrl="~/Reports/CustomerReport.aspx" 
                                    CssClass="dropdown-item">
                                    Customer Report
                                </asp:HyperLink>
                            </div>
                        </li>
                    </ul>
                    
                    <!-- User Menu -->
                    <ul class="navbar-nav">
                        <asp:LoginView ID="HeadLoginView" runat="server" EnableViewState="false">
                            <AnonymousTemplate>
                                <li class="nav-item">
                                    <asp:LoginStatus ID="HeadLoginStatus" runat="server" 
                                        LogoutAction="Redirect" 
                                        LogoutText="Log In" 
                                        LogoutPageUrl="~/Account/Login.aspx" 
                                        CssClass="nav-link" />
                                </li>
                            </AnonymousTemplate>
                            <LoggedInTemplate>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" href="#" id="userDropdown" 
                                       role="button" data-toggle="dropdown">
                                        Welcome, <asp:LoginName ID="HeadLoginName" runat="server" />
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-right">
                                        <asp:HyperLink ID="lnkProfile" runat="server" 
                                            NavigateUrl="~/Account/Profile.aspx" 
                                            CssClass="dropdown-item">
                                            My Profile
                                        </asp:HyperLink>
                                        <asp:HyperLink ID="lnkSettings" runat="server" 
                                            NavigateUrl="~/Account/Settings.aspx" 
                                            CssClass="dropdown-item">
                                            Settings
                                        </asp:HyperLink>
                                        <div class="dropdown-divider"></div>
                                        <asp:LoginStatus ID="HeadLoginStatus" runat="server" 
                                            LogoutAction="Redirect" 
                                            LogoutText="Log Out" 
                                            LogoutPageUrl="~/Default.aspx" 
                                            CssClass="dropdown-item" />
                                    </div>
                                </li>
                            </LoggedInTemplate>
                        </asp:LoginView>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Breadcrumb Navigation -->
        <nav aria-label="breadcrumb" class="bg-light">
            <div class="container">
                <asp:SiteMapPath ID="SiteMapPath1" runat="server" 
                    CssClass="breadcrumb"
                    CurrentNodeStyle-CssClass="breadcrumb-item active"
                    NodeStyle-CssClass="breadcrumb-item"
                    RootNodeStyle-CssClass="breadcrumb-item" />
            </div>
        </nav>

        <!-- Main Content Area -->
        <main class="container-fluid">
            <!-- Global Messages -->
            <asp:Panel ID="GlobalMessagePanel" runat="server" CssClass="alert" Visible="false">
                <asp:Label ID="GlobalMessageLabel" runat="server" />
                <button type="button" class="close" data-dismiss="alert">
                    <span>&times;</span>
                </button>
            </asp:Panel>
            
            <!-- Content from child pages -->
            <asp:ContentPlaceHolder ID="MainContent" runat="server">
            </asp:ContentPlaceHolder>
        </main>

        <!-- Footer -->
        <footer class="bg-dark text-light mt-5">
            <div class="container">
                <div class="row py-4">
                    <div class="col-md-6">
                        <h5>Enterprise Application</h5>
                        <p>© <%: DateTime.Now.Year %> Company Name. All rights reserved.</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Quick Links</h6>
                        <ul class="list-unstyled">
                            <li><asp:HyperLink ID="lnkSupport" runat="server" NavigateUrl="~/Support.aspx">Support</asp:HyperLink></li>
                            <li><asp:HyperLink ID="lnkPrivacy" runat="server" NavigateUrl="~/Privacy.aspx">Privacy Policy</asp:HyperLink></li>
                            <li><asp:HyperLink ID="lnkTerms" runat="server" NavigateUrl="~/Terms.aspx">Terms of Service</asp:HyperLink></li>
                        </ul>
                    </div>
                </div>
            </div>
        </footer>

        <!-- JavaScript -->
        <asp:PlaceHolder runat="server">
            <%: System.Web.Optimization.Scripts.Render("~/bundles/jquery") %>
            <%: System.Web.Optimization.Scripts.Render("~/bundles/bootstrap") %>
        </asp:PlaceHolder>
        
        <!-- Additional JavaScript from content pages -->
        <asp:ContentPlaceHolder ID="ScriptContent" runat="server"></asp:ContentPlaceHolder>
    </form>
</body>
</html>
```

### 1.2 Master Page Code-Behind (Site.Master.cs)

```csharp
using System;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebFormsApp
{
    public partial class SiteMaster : MasterPage
    {
        protected void Page_Init(object sender, EventArgs e)
        {
            // Security headers
            Response.Headers.Add("X-Frame-Options", "SAMEORIGIN");
            Response.Headers.Add("X-Content-Type-Options", "nosniff");
            Response.Headers.Add("X-XSS-Protection", "1; mode=block");
        }
        
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                SetupNavigation();
                CheckForGlobalMessages();
            }
        }
        
        private void SetupNavigation()
        {
            // Highlight current section based on URL
            var currentPath = Request.AppRelativeCurrentExecutionFilePath.ToLower();
            
            if (currentPath.Contains("/customers/"))
            {
                lnkCustomers.CssClass += " active";
            }
            else if (currentPath.Contains("/orders/"))
            {
                lnkOrders.CssClass += " active";
            }
            else if (currentPath.Contains("/reports/"))
            {
                // Handle reports dropdown
                var reportsDropdown = FindControl("reportsDropdown");
                if (reportsDropdown != null)
                {
                    ((WebControl)reportsDropdown).CssClass += " active";
                }
            }
        }
        
        private void CheckForGlobalMessages()
        {
            // Check for global messages in session
            if (Session["GlobalMessage"] != null)
            {
                var message = Session["GlobalMessage"].ToString();
                var messageType = Session["GlobalMessageType"]?.ToString() ?? "info";
                
                ShowGlobalMessage(message, messageType);
                
                // Clear message after displaying
                Session.Remove("GlobalMessage");
                Session.Remove("GlobalMessageType");
            }
        }
        
        public void ShowGlobalMessage(string message, string messageType = "info")
        {
            var cssClass = "alert ";
            switch (messageType.ToLower())
            {
                case "success":
                    cssClass += "alert-success";
                    break;
                case "error":
                case "danger":
                    cssClass += "alert-danger";
                    break;
                case "warning":
                    cssClass += "alert-warning";
                    break;
                default:
                    cssClass += "alert-info";
                    break;
            }
            
            GlobalMessagePanel.CssClass = cssClass + " alert-dismissible";
            GlobalMessageLabel.Text = message;
            GlobalMessagePanel.Visible = true;
        }
        
        // Public properties for child pages to access
        public Label GlobalMessage => GlobalMessageLabel;
        public Panel GlobalMessageContainer => GlobalMessagePanel;
    }
}
```

## 2. Hierarchical Master Pages

### 2.1 Admin Master Page (Admin.Master)

```aspx
<%@ Master Language="C#" MasterPageFile="~/Site.Master" 
    AutoEventWireup="true" CodeBehind="Admin.master.cs" 
    Inherits="WebFormsApp.AdminMaster" %>

<asp:Content ID="MetaContent" ContentPlaceHolderID="MetaContent" runat="server">
    <meta name="robots" content="noindex, nofollow" />
</asp:Content>

<asp:Content ID="CssContent" ContentPlaceHolderID="CssContent" runat="server">
    <link href="~/Content/admin.css" rel="stylesheet" />
</asp:Content>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
    <div class="admin-layout">
        <!-- Admin Sidebar -->
        <nav class="admin-sidebar bg-dark">
            <div class="sidebar-header">
                <h4 class="text-white">Administration</h4>
            </div>
            
            <ul class="nav flex-column">
                <li class="nav-item">
                    <asp:HyperLink ID="lnkDashboard" runat="server" 
                        NavigateUrl="~/Admin/Dashboard.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </asp:HyperLink>
                </li>
                <li class="nav-item">
                    <asp:HyperLink ID="lnkUsers" runat="server" 
                        NavigateUrl="~/Admin/Users.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-users"></i> User Management
                    </asp:HyperLink>
                </li>
                <li class="nav-item">
                    <asp:HyperLink ID="lnkRoles" runat="server" 
                        NavigateUrl="~/Admin/Roles.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-user-shield"></i> Role Management
                    </asp:HyperLink>
                </li>
                <li class="nav-item">
                    <asp:HyperLink ID="lnkSettings" runat="server" 
                        NavigateUrl="~/Admin/Settings.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-cogs"></i> System Settings
                    </asp:HyperLink>
                </li>
                <li class="nav-item">
                    <asp:HyperLink ID="lnkLogs" runat="server" 
                        NavigateUrl="~/Admin/Logs.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-file-alt"></i> System Logs
                    </asp:HyperLink>
                </li>
                <li class="nav-item">
                    <asp:HyperLink ID="lnkBackup" runat="server" 
                        NavigateUrl="~/Admin/Backup.aspx" 
                        CssClass="nav-link text-white">
                        <i class="fas fa-database"></i> Backup & Restore
                    </asp:HyperLink>
                </li>
            </ul>
        </nav>
        
        <!-- Admin Content Area -->
        <main class="admin-content">
            <!-- Admin Toolbar -->
            <div class="admin-toolbar bg-light border-bottom">
                <div class="d-flex justify-content-between align-items-center p-3">
                    <div>
                        <h5 class="mb-0">
                            <asp:Label ID="lblPageTitle" runat="server" />
                        </h5>
                        <small class="text-muted">
                            <asp:Label ID="lblPageDescription" runat="server" />
                        </small>
                    </div>
                    <div>
                        <asp:Panel ID="AdminActionsPanel" runat="server">
                            <!-- Admin-specific actions will be added by child pages -->
                        </asp:Panel>
                    </div>
                </div>
            </div>
            
            <!-- Admin Page Content -->
            <div class="admin-page-content p-4">
                <asp:ContentPlaceHolder ID="AdminContent" runat="server">
                </asp:ContentPlaceHolder>
            </div>
        </main>
    </div>
</asp:Content>

<asp:Content ID="ScriptContent" ContentPlaceHolderID="ScriptContent" runat="server">
    <script src="~/Scripts/admin.js"></script>
    <asp:ContentPlaceHolder ID="AdminScriptContent" runat="server">
    </asp:ContentPlaceHolder>
</asp:Content>
```

### 2.2 Admin Master Code-Behind

```csharp
using System;
using System.Web.UI;
using System.Web.Security;

namespace WebFormsApp
{
    public partial class AdminMaster : MasterPage
    {
        protected void Page_Init(object sender, EventArgs e)
        {
            // Security check for admin access
            if (!User.IsInRole("Administrator") && !User.IsInRole("SuperUser"))
            {
                Response.Redirect("~/Unauthorized.aspx");
            }
        }
        
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                SetupAdminNavigation();
                SetPageInfo();
            }
        }
        
        private void SetupAdminNavigation()
        {
            var currentPath = Request.AppRelativeCurrentExecutionFilePath.ToLower();
            
            // Highlight current admin section
            if (currentPath.Contains("/admin/dashboard"))
                lnkDashboard.CssClass += " active";
            else if (currentPath.Contains("/admin/users"))
                lnkUsers.CssClass += " active";
            else if (currentPath.Contains("/admin/roles"))
                lnkRoles.CssClass += " active";
            else if (currentPath.Contains("/admin/settings"))
                lnkSettings.CssClass += " active";
            else if (currentPath.Contains("/admin/logs"))
                lnkLogs.CssClass += " active";
            else if (currentPath.Contains("/admin/backup"))
                lnkBackup.CssClass += " backup";
        }
        
        private void SetPageInfo()
        {
            // Get page info from child page if available
            var contentPage = Page;
            if (contentPage != null)
            {
                lblPageTitle.Text = !string.IsNullOrEmpty(contentPage.Title) 
                    ? contentPage.Title 
                    : "Administration";
                    
                // Check if child page has a description property
                var descriptionProperty = contentPage.GetType().GetProperty("PageDescription");
                if (descriptionProperty != null)
                {
                    var description = descriptionProperty.GetValue(contentPage) as string;
                    lblPageDescription.Text = description ?? string.Empty;
                }
            }
        }
        
        // Public properties for child pages
        public string PageTitle
        {
            get => lblPageTitle.Text;
            set => lblPageTitle.Text = value;
        }
        
        public string PageDescription
        {
            get => lblPageDescription.Text;
            set => lblPageDescription.Text = value;
        }
        
        public Panel AdminActions => AdminActionsPanel;
    }
}
```

## 3. Dynamic Master Page Selection

### 3.1 Dynamic Master Page Implementation

```csharp
public partial class DynamicMasterPage : Page
{
    protected override void OnPreInit(EventArgs e)
    {
        // Determine master page based on various criteria
        DetermineMasterPage();
        base.OnPreInit(e);
    }
    
    private void DetermineMasterPage()
    {
        // 1. Check for mobile devices
        if (IsMobileDevice())
        {
            MasterPageFile = "~/Mobile.Master";
            return;
        }
        
        // 2. Check user preferences
        var userPreference = GetUserMasterPagePreference();
        if (!string.IsNullOrEmpty(userPreference))
        {
            MasterPageFile = userPreference;
            return;
        }
        
        // 3. Check for admin sections
        if (Request.Url.AbsolutePath.ToLower().Contains("/admin/"))
        {
            MasterPageFile = "~/Admin.Master";
            return;
        }
        
        // 4. Check for public sections
        if (Request.Url.AbsolutePath.ToLower().Contains("/public/"))
        {
            MasterPageFile = "~/Public.Master";
            return;
        }
        
        // 5. Check query string override
        var masterOverride = Request.QueryString["master"];
        if (!string.IsNullOrEmpty(masterOverride))
        {
            switch (masterOverride.ToLower())
            {
                case "mobile":
                    MasterPageFile = "~/Mobile.Master";
                    break;
                case "print":
                    MasterPageFile = "~/Print.Master";
                    break;
                case "minimal":
                    MasterPageFile = "~/Minimal.Master";
                    break;
                default:
                    MasterPageFile = "~/Site.Master";
                    break;
            }
            return;
        }
        
        // Default master page
        MasterPageFile = "~/Site.Master";
    }
    
    private bool IsMobileDevice()
    {
        // Check user agent for mobile devices
        var userAgent = Request.UserAgent?.ToLower() ?? string.Empty;
        
        var mobileKeywords = new[] { "mobile", "android", "iphone", "ipad", "windows phone" };
        return mobileKeywords.Any(keyword => userAgent.Contains(keyword));
    }
    
    private string GetUserMasterPagePreference()
    {
        // Check user profile for master page preference
        if (User.Identity.IsAuthenticated)
        {
            var preference = Session["UserMasterPagePreference"] as string;
            if (!string.IsNullOrEmpty(preference))
            {
                return preference;
            }
        }
        
        return null;
    }
}
```

### 3.2 Mobile Master Page

```aspx
<%@ Master Language="C#" AutoEventWireup="true" CodeBehind="Mobile.master.cs" Inherits="WebFormsApp.MobileMaster" %>

<!DOCTYPE html>
<html lang="en">
<head runat="server">
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
    <title><%: Page.Title %> - Mobile</title>
    
    <!-- Mobile-optimized CSS -->
    <link href="~/Content/mobile.css" rel="stylesheet" />
    <link href="~/Content/bootstrap-mobile.css" rel="stylesheet" />
</head>

<body>
    <form runat="server">
        <!-- Mobile Header -->
        <header class="mobile-header">
            <div class="header-content">
                <button class="menu-toggle" type="button" onclick="toggleMobileMenu()">
                    ☰
                </button>
                <h1 class="mobile-title"><%: Page.Title %></h1>
                <asp:LoginView ID="MobileLoginView" runat="server">
                    <LoggedInTemplate>
                        <span class="user-info">
                            <asp:LoginName ID="MobileLoginName" runat="server" />
                        </span>
                    </LoggedInTemplate>
                </asp:LoginView>
            </div>
        </header>
        
        <!-- Mobile Navigation -->
        <nav class="mobile-nav" id="mobileMenu">
            <ul class="nav-list">
                <li><asp:HyperLink ID="lnkHome" runat="server" NavigateUrl="~/Default.aspx">Home</asp:HyperLink></li>
                <li><asp:HyperLink ID="lnkCustomers" runat="server" NavigateUrl="~/Customers/CustomerList.aspx">Customers</asp:HyperLink></li>
                <li><asp:HyperLink ID="lnkOrders" runat="server" NavigateUrl="~/Orders/OrderList.aspx">Orders</asp:HyperLink></li>
                <li><asp:HyperLink ID="lnkReports" runat="server" NavigateUrl="~/Reports/Default.aspx">Reports</asp:HyperLink></li>
            </ul>
        </nav>
        
        <!-- Mobile Content -->
        <main class="mobile-content">
            <asp:ContentPlaceHolder ID="MobileContent" runat="server">
            </asp:ContentPlaceHolder>
        </main>
        
        <!-- Mobile Footer -->
        <footer class="mobile-footer">
            <p>&copy; <%: DateTime.Now.Year %> Company Name</p>
            <asp:HyperLink ID="lnkDesktopSite" runat="server" 
                NavigateUrl="~/SwitchToDesktop.aspx" 
                CssClass="desktop-link">
                View Desktop Site
            </asp:HyperLink>
        </footer>
        
        <!-- Mobile JavaScript -->
        <script src="~/Scripts/mobile.js"></script>
    </form>
</body>
</html>
```

## 4. Master Page Migration Patterns

### 4.1 Layout Component Migration Strategy

```typescript
// Modern React Layout Component (Target Architecture)
interface LayoutProps {
  title?: string;
  description?: string;
  showSidebar?: boolean;
  children: React.ReactNode;
}

export const MainLayout: React.FC<LayoutProps> = ({ 
  title, 
  description, 
  showSidebar = true, 
  children 
}) => {
  const { user } = useAuth();
  const [globalMessage, setGlobalMessage] = useGlobalMessage();
  
  return (
    <div className="layout-container">
      {/* Header Navigation */}
      <Header user={user} />
      
      {/* Breadcrumb */}
      <Breadcrumb />
      
      {/* Global Messages */}
      {globalMessage && (
        <GlobalMessage 
          message={globalMessage.text} 
          type={globalMessage.type} 
          onDismiss={() => setGlobalMessage(null)} 
        />
      )}
      
      <div className="main-container">
        {/* Sidebar */}
        {showSidebar && <Sidebar />}
        
        {/* Main Content */}
        <main className="content-area">
          {title && (
            <div className="page-header">
              <h1>{title}</h1>
              {description && <p className="page-description">{description}</p>}
            </div>
          )}
          {children}
        </main>
      </div>
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

// Usage in pages
const CustomerList: React.FC = () => {
  return (
    <MainLayout title="Customer Management" description="Manage your customers">
      <CustomerListContent />
    </MainLayout>
  );
};
```

### 4.2 Transitional Pattern - WebForms to Modern

```csharp
// Transitional base page that can work with both master pages and modern layouts
public class TransitionalBasePage : Page
{
    protected override void OnPreInit(EventArgs e)
    {
        // Check if we should use legacy master page or modern layout
        if (ShouldUseLegacyMaster())
        {
            MasterPageFile = "~/Site.Master";
        }
        else
        {
            // Use API-based rendering for modern layout
            MasterPageFile = "~/Modern.Master";
        }
        
        base.OnPreInit(e);
    }
    
    private bool ShouldUseLegacyMaster()
    {
        // Feature toggle for gradual migration
        var useLegacy = ConfigurationManager.AppSettings["UseLegacyMaster"] == "true";
        var userOptIn = Session["UseModernLayout"] as bool? ?? false;
        
        // Allow per-user opt-in to modern layout
        return useLegacy && !userOptIn;
    }
    
    protected void Page_Load(object sender, EventArgs e)
    {
        // Setup modern layout context if needed
        if (!ShouldUseLegacyMaster())
        {
            SetupModernLayoutContext();
        }
    }
    
    private void SetupModernLayoutContext()
    {
        // Prepare data for modern layout components
        var layoutContext = new
        {
            PageTitle = Page.Title,
            UserName = User.Identity.Name,
            NavigationItems = GetNavigationItems(),
            GlobalMessages = GetGlobalMessages()
        };
        
        // Make available to client-side
        var script = $"window.layoutContext = {JsonConvert.SerializeObject(layoutContext)};";
        ClientScript.RegisterStartupScript(this.GetType(), "LayoutContext", script, true);
    }
}
```

## 5. Performance Optimization Patterns

### 5.1 Master Page Caching Strategy

```csharp
public partial class OptimizedSiteMaster : MasterPage
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if (!IsPostBack)
        {
            LoadNavigationWithCaching();
            LoadUserPreferencesWithCaching();
        }
    }
    
    private void LoadNavigationWithCaching()
    {
        var cacheKey = $"Navigation_{User.Identity.Name}_{GetUserRoles()}";
        var navigationItems = HttpContext.Current.Cache[cacheKey] as List<NavigationItem>;
        
        if (navigationItems == null)
        {
            navigationItems = NavigationService.GetNavigationForUser(User.Identity.Name);
            
            // Cache for 30 minutes
            HttpContext.Current.Cache.Insert(
                cacheKey, 
                navigationItems, 
                null, 
                DateTime.Now.AddMinutes(30), 
                TimeSpan.Zero);
        }
        
        RenderNavigation(navigationItems);
    }
    
    private void LoadUserPreferencesWithCaching()
    {
        var cacheKey = $"UserPrefs_{User.Identity.Name}";
        var preferences = HttpContext.Current.Cache[cacheKey] as UserPreferences;
        
        if (preferences == null)
        {
            preferences = UserService.GetUserPreferences(User.Identity.Name);
            
            // Cache for 1 hour
            HttpContext.Current.Cache.Insert(
                cacheKey, 
                preferences, 
                null, 
                DateTime.Now.AddHours(1), 
                TimeSpan.Zero);
        }
        
        ApplyUserPreferences(preferences);
    }
    
    private string GetUserRoles()
    {
        var roles = new List<string>();
        if (User.IsInRole("Administrator")) roles.Add("Admin");
        if (User.IsInRole("Manager")) roles.Add("Manager");
        if (User.IsInRole("User")) roles.Add("User");
        
        return string.Join(",", roles);
    }
}
```

### 5.2 Master Page ViewState Optimization

```csharp
public partial class OptimizedMaster : MasterPage
{
    protected override void OnInit(EventArgs e)
    {
        base.OnInit(e);
        
        // Disable ViewState for navigation controls that don't need it
        DisableViewStateForStaticControls();
    }
    
    private void DisableViewStateForStaticControls()
    {
        // Navigation links don't need ViewState
        lnkHome.EnableViewState = false;
        lnkCustomers.EnableViewState = false;
        lnkOrders.EnableViewState = false;
        
        // Login view doesn't need ViewState for display
        HeadLoginView.EnableViewState = false;
        
        // Footer links don't need ViewState
        lnkSupport.EnableViewState = false;
        lnkPrivacy.EnableViewState = false;
        lnkTerms.EnableViewState = false;
    }
    
    protected override object SaveViewState()
    {
        // Only save ViewState for controls that actually need it
        var viewState = base.SaveViewState();
        
        // Log ViewState size for monitoring
        if (viewState != null)
        {
            var viewStateString = Convert.ToBase64String(
                System.Web.UI.LosFormatter.Serialize(viewState));
            
            if (viewStateString.Length > 10240) // > 10KB
            {
                System.Diagnostics.Debug.WriteLine($"Large ViewState detected: {viewStateString.Length} bytes");
            }
        }
        
        return viewState;
    }
}
```

---

**Master Page Analysis Status**: ✅ COMPLETE  
**Pattern Coverage**: ✅ COMPREHENSIVE IMPLEMENTATION EXAMPLES  
**Migration Strategy**: ✅ MODERN LAYOUT MIGRATION PATTERNS  
**Performance Optimization**: ✅ CACHING AND VIEWSTATE OPTIMIZATION

*Code Archaeologist: Master Page Patterns Analysis Complete*  
*Memory Key: hive/analysis/patterns/webforms-master-pages*