# WebForms Design Patterns Catalog

## Overview
This catalog documents common design patterns found in ASP.NET WebForms applications, their characteristics, and modernization approaches.

## Pattern Categories

### 1. Page Patterns

#### 1.1 Master-Detail Pattern
**Description**: Master page displays list, detail page shows individual record
**Implementation**:
```csharp
// Master Page
GridView → RowCommand → Response.Redirect("Details.aspx?id=" + id)

// Detail Page
Page_Load → Request.QueryString["id"] → Load Record → Display
```
**Modernization**: Convert to SPA with routing or Blazor components

#### 1.2 Wizard Pattern
**Description**: Multi-step process using Wizard control or custom implementation
**Implementation**:
```csharp
<asp:Wizard ID="Wizard1" runat="server">
    <WizardSteps>
        <asp:WizardStep>Step 1</asp:WizardStep>
        <asp:WizardStep>Step 2</asp:WizardStep>
    </WizardSteps>
</asp:Wizard>
```
**Modernization**: State machine pattern with API backend

#### 1.3 Dashboard Pattern
**Description**: Multiple data views on single page with UpdatePanels
**Implementation**:
```csharp
Multiple UpdatePanels → Async updates → Independent refresh
```
**Modernization**: Component-based architecture with real-time updates

### 2. Data Access Patterns

#### 2.1 Repository Pattern Implementation
**Description**: Data access abstraction layer
**Implementation**:
```csharp
public interface ICustomerRepository
{
    Customer GetById(int id);
    IEnumerable<Customer> GetAll();
    void Save(Customer customer);
    void Delete(int id);
}

// ObjectDataSource binding
<asp:ObjectDataSource TypeName="CustomerRepository" 
    SelectMethod="GetAll" />
```
**Assessment**: Good separation, easy to modernize

#### 2.2 Direct SQL Pattern
**Description**: SQL commands in code-behind
**Implementation**:
```csharp
protected void btnSave_Click(object sender, EventArgs e)
{
    using (SqlConnection conn = new SqlConnection(connString))
    {
        SqlCommand cmd = new SqlCommand(
            "INSERT INTO Customers VALUES (@Name)", conn);
        cmd.Parameters.AddWithValue("@Name", txtName.Text);
        cmd.ExecuteNonQuery();
    }
}
```
**Assessment**: High risk, requires refactoring

#### 2.3 Stored Procedure Pattern
**Description**: All data access through stored procedures
**Implementation**:
```csharp
SqlCommand cmd = new SqlCommand("sp_GetCustomers", conn);
cmd.CommandType = CommandType.StoredProcedure;
```
**Assessment**: Better security, but tight coupling

### 3. State Management Patterns

#### 3.1 ViewState Optimization Pattern
**Description**: Selective ViewState usage
**Implementation**:
```csharp
// Disable for read-only controls
GridView1.EnableViewState = false;

// Store ViewState server-side
protected override PageStatePersister PageStatePersister
{
    get { return new SessionPageStatePersister(this); }
}
```
**Modernization**: Client-side state management

#### 3.2 Session Facade Pattern
**Description**: Wrapper for session management
**Implementation**:
```csharp
public static class SessionManager
{
    public static User CurrentUser
    {
        get { return (User)HttpContext.Current.Session["User"]; }
        set { HttpContext.Current.Session["User"] = value; }
    }
}
```
**Modernization**: JWT tokens or distributed cache

#### 3.3 Cross-Page Posting Pattern
**Description**: Posting data between pages
**Implementation**:
```csharp
// Source page
<asp:Button PostBackUrl="~/Target.aspx" />

// Target page
if (PreviousPage != null && PreviousPage.IsCrossPagePostBack)
{
    TextBox txtPrev = (TextBox)PreviousPage.FindControl("txtData");
}
```
**Modernization**: API-based data transfer

### 4. UI Patterns

#### 4.1 Dynamic Control Creation
**Description**: Creating controls at runtime
**Implementation**:
```csharp
protected void Page_Init(object sender, EventArgs e)
{
    for (int i = 0; i < count; i++)
    {
        TextBox txt = new TextBox();
        txt.ID = "txt" + i;
        PlaceHolder1.Controls.Add(txt);
    }
}
```
**Assessment**: Complex state management
**Modernization**: Component-based dynamic rendering

#### 4.2 Composite Control Pattern
**Description**: Custom controls combining multiple controls
**Implementation**:
```csharp
public class AddressControl : CompositeControl
{
    protected override void CreateChildControls()
    {
        Controls.Add(new TextBox { ID = "txtStreet" });
        Controls.Add(new TextBox { ID = "txtCity" });
    }
}
```
**Modernization**: Reusable components in modern frameworks

#### 4.3 Template Control Pattern
**Description**: Repeater/DataList with templates
**Implementation**:
```csharp
<asp:Repeater ID="rptItems" runat="server">
    <ItemTemplate>
        <div><%# Eval("Name") %></div>
    </ItemTemplate>
</asp:Repeater>
```
**Modernization**: Component templates with data binding

### 5. Business Logic Patterns

#### 5.1 Page Controller Pattern
**Description**: Business logic in code-behind
**Implementation**:
```csharp
public partial class OrderPage : Page
{
    protected void btnSubmit_Click(object sender, EventArgs e)
    {
        // Validation
        // Business rules
        // Data access
        // UI update
    }
}
```
**Assessment**: Poor separation of concerns
**Modernization**: MVC/MVP pattern

#### 5.2 Service Layer Pattern
**Description**: Business logic in separate service classes
**Implementation**:
```csharp
public class OrderService
{
    public OrderResult ProcessOrder(Order order)
    {
        // Business logic here
    }
}

// Page code
OrderService service = new OrderService();
var result = service.ProcessOrder(order);
```
**Assessment**: Good separation, easier to test
**Modernization**: Direct reuse in modern architecture

#### 5.3 Transaction Script Pattern
**Description**: Procedural transaction handling
**Implementation**:
```csharp
public void TransferFunds(int fromAccount, int toAccount, decimal amount)
{
    using (TransactionScope scope = new TransactionScope())
    {
        // Multiple database operations
        scope.Complete();
    }
}
```
**Modernization**: Domain-driven design patterns

### 6. Integration Patterns

#### 6.1 Web Service Integration
**Description**: ASMX web service consumption
**Implementation**:
```csharp
ServiceReference.WebService service = new ServiceReference.WebService();
var result = service.GetData();
```
**Modernization**: REST API integration

#### 6.2 WCF Service Pattern
**Description**: WCF service integration
**Implementation**:
```csharp
using (var client = new ServiceClient())
{
    var result = client.Operation();
}
```
**Modernization**: HTTP client with REST APIs

#### 6.3 Message Queue Pattern
**Description**: Asynchronous processing
**Implementation**:
```csharp
// Send message
MessageQueue queue = new MessageQueue(@".\private$\orders");
queue.Send(orderMessage);

// Separate processor handles messages
```
**Modernization**: Modern message brokers (Azure Service Bus, RabbitMQ)

### 7. Security Patterns

#### 7.1 Forms Authentication Pattern
**Description**: Custom authentication implementation
**Implementation**:
```csharp
if (ValidateUser(username, password))
{
    FormsAuthentication.SetAuthCookie(username, false);
    Response.Redirect("Default.aspx");
}
```
**Modernization**: Identity framework or external providers

#### 7.2 Role-Based Authorization
**Description**: Role checking in pages
**Implementation**:
```csharp
if (!User.IsInRole("Admin"))
{
    Response.Redirect("AccessDenied.aspx");
}
```
**Modernization**: Policy-based authorization

#### 7.3 Custom Principal Pattern
**Description**: Extended user information
**Implementation**:
```csharp
public class CustomPrincipal : IPrincipal
{
    public string Email { get; set; }
    public string Department { get; set; }
}
```
**Modernization**: Claims-based identity

### 8. Performance Patterns

#### 8.1 Output Caching Pattern
**Description**: Page and control caching
**Implementation**:
```csharp
<%@ OutputCache Duration="3600" VaryByParam="id" %>
```
**Modernization**: Distributed caching strategies

#### 8.2 Lazy Loading Pattern
**Description**: Deferred data loading
**Implementation**:
```csharp
private DataSet _data;
public DataSet Data
{
    get 
    { 
        if (_data == null)
            _data = LoadData();
        return _data;
    }
}
```
**Modernization**: Async/await patterns

#### 8.3 Connection Pooling Pattern
**Description**: Efficient database connections
**Implementation**:
```csharp
// Connection string with pooling
"...;Pooling=true;Min Pool Size=5;Max Pool Size=100"
```
**Modernization**: Modern ORM connection management

## Pattern Assessment Matrix

| Pattern | Complexity | Risk | Modernization Effort |
|---------|------------|------|---------------------|
| Master-Detail | Low | Low | Low |
| Direct SQL | High | High | High |
| ViewState Heavy | Medium | Medium | Medium |
| Service Layer | Low | Low | Low |
| Page Controller | High | Medium | High |
| Custom Controls | High | Medium | High |

## Modernization Priority Guide

### High Priority (Address First)
1. Direct SQL in code-behind
2. Heavy ViewState usage
3. God page anti-pattern
4. No separation of concerns

### Medium Priority
1. Session state dependencies
2. Custom authentication
3. Tight coupling to controls
4. Synchronous operations

### Low Priority (Address Last)
1. Well-structured service layers
2. Repository patterns
3. Output caching
4. Standard controls usage

## Best Practices for Pattern Migration

### 1. Identify Pattern Usage
- Code analysis tools
- Manual code review
- Pattern detection scripts

### 2. Assess Business Impact
- Critical path analysis
- User impact assessment
- Risk evaluation

### 3. Plan Migration Strategy
- Pattern-by-pattern approach
- Feature-based migration
- Risk-based prioritization

### 4. Execute Migration
- Maintain tests throughout
- Parallel implementation
- Gradual cutover

### 5. Validate Results
- Performance comparison
- Functionality verification
- User acceptance testing

---

*This catalog serves as a reference for teams assessing and modernizing WebForms applications using pattern-based analysis.*