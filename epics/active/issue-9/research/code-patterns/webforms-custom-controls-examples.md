# ASP.NET WebForms Custom Server Controls Implementation Patterns

**Code Archaeologist Analysis**  
**Date**: August 15, 2025  
**Task**: Custom Server Control Development Patterns  
**Coordination**: Hive Mind Control Architecture Analysis  

---

## Executive Summary

This document provides comprehensive examples of ASP.NET WebForms custom server control development patterns, including composite controls, rendering patterns, state management, and migration strategies to modern web components.

## 1. Basic Custom Server Control

### 1.1 Simple Custom Control Implementation

```csharp
using System;
using System.ComponentModel;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Drawing;

[DefaultProperty("Text")]
[ToolboxData("<{0}:SimpleCustomControl runat=server></{0}:SimpleCustomControl>")]
public class SimpleCustomControl : WebControl, INamingContainer
{
    #region Properties
    
    [Bindable(true)]
    [Category("Appearance")]
    [DefaultValue("")]
    [Localizable(true)]
    [Description("The text displayed by the control")]
    public string Text
    {
        get { return ViewState["Text"] as string ?? string.Empty; }
        set { ViewState["Text"] = value; }
    }
    
    [Bindable(true)]
    [Category("Appearance")]
    [DefaultValue(typeof(Color), "Blue")]
    [Description("The color of the text")]
    public Color TextColor
    {
        get 
        { 
            object color = ViewState["TextColor"];
            return color != null ? (Color)color : Color.Blue;
        }
        set { ViewState["TextColor"] = value; }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(false)]
    [Description("Indicates whether the control displays in uppercase")]
    public bool UpperCase
    {
        get { return ViewState["UpperCase"] as bool? ?? false; }
        set { ViewState["UpperCase"] = value; }
    }
    
    #endregion
    
    #region Rendering
    
    protected override void RenderContents(HtmlTextWriter output)
    {
        var displayText = Text;
        if (UpperCase)
            displayText = displayText.ToUpper();
            
        output.AddStyleAttribute(HtmlTextWriterStyle.Color, ColorTranslator.ToHtml(TextColor));
        output.AddStyleAttribute(HtmlTextWriterStyle.FontWeight, "bold");
        output.RenderBeginTag(HtmlTextWriterTag.Span);
        output.WriteEncodedText(displayText);
        output.RenderEndTag();
    }
    
    protected override HtmlTextWriterTag TagKey
    {
        get { return HtmlTextWriterTag.Div; }
    }
    
    #endregion
    
    #region Designer Support
    
    protected override void OnPreRender(EventArgs e)
    {
        base.OnPreRender(e);
        
        // Register client script if needed
        if (!Page.ClientScript.IsClientScriptIncludeRegistered("SimpleCustomControl"))
        {
            Page.ClientScript.RegisterClientScriptInclude(
                "SimpleCustomControl",
                Page.ClientScript.GetWebResourceUrl(this.GetType(), "SimpleCustomControl.js"));
        }
    }
    
    #endregion
}
```

## 2. Advanced Composite Control

### 2.1 Enterprise Search Control

```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Web.UI;
using System.Web.UI.WebControls;

[DefaultProperty("SearchText")]
[ToolboxData("<{0}:EnterpriseSearchControl runat=server></{0}:EnterpriseSearchControl>")]
public class EnterpriseSearchControl : CompositeControl, INamingContainer
{
    #region Child Controls
    
    private TextBox _searchTextBox;
    private Button _searchButton;
    private Button _clearButton;
    private DropDownList _searchTypeDropDown;
    private Panel _suggestionsPanel;
    private UpdatePanel _updatePanel;
    private Timer _searchTimer;
    
    #endregion
    
    #region Events
    
    public event EventHandler<SearchEventArgs> Search;
    public event EventHandler<SearchEventArgs> SearchTextChanged;
    public event EventHandler ClearSearch;
    
    #endregion
    
    #region Properties
    
    [Bindable(true)]
    [Category("Data")]
    [DefaultValue("")]
    [Description("The search text")]
    public string SearchText
    {
        get 
        { 
            EnsureChildControls();
            return _searchTextBox.Text; 
        }
        set 
        { 
            EnsureChildControls();
            _searchTextBox.Text = value; 
        }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(true)]
    [Description("Enable auto-suggestions")]
    public bool EnableAutoSuggest
    {
        get { return ViewState["EnableAutoSuggest"] as bool? ?? true; }
        set { ViewState["EnableAutoSuggest"] = value; }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(500)]
    [Description("Auto-suggest delay in milliseconds")]
    public int AutoSuggestDelay
    {
        get { return ViewState["AutoSuggestDelay"] as int? ?? 500; }
        set { ViewState["AutoSuggestDelay"] = value; }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(3)]
    [Description("Minimum characters for auto-suggest")]
    public int MinimumPrefixLength
    {
        get { return ViewState["MinimumPrefixLength"] as int? ?? 3; }
        set { ViewState["MinimumPrefixLength"] = value; }
    }
    
    [Bindable(true)]
    [Category("Data")]
    [Description("Search types available")]
    public List<SearchType> SearchTypes
    {
        get { return ViewState["SearchTypes"] as List<SearchType> ?? new List<SearchType>(); }
        set 
        { 
            ViewState["SearchTypes"] = value;
            if (_searchTypeDropDown != null)
            {
                PopulateSearchTypes();
            }
        }
    }
    
    [Bindable(true)]
    [Category("Data")]
    [DefaultValue("")]
    [Description("Selected search type")]
    public string SelectedSearchType
    {
        get 
        { 
            EnsureChildControls();
            return _searchTypeDropDown.SelectedValue; 
        }
        set 
        { 
            EnsureChildControls();
            _searchTypeDropDown.SelectedValue = value; 
        }
    }
    
    [Bindable(true)]
    [Category("Appearance")]
    [DefaultValue("Search...")]
    [Description("Placeholder text for the search box")]
    public string PlaceholderText
    {
        get { return ViewState["PlaceholderText"] as string ?? "Search..."; }
        set 
        { 
            ViewState["PlaceholderText"] = value;
            if (_searchTextBox != null)
            {
                _searchTextBox.Attributes["placeholder"] = value;
            }
        }
    }
    
    [Bindable(true)]
    [Category("Layout")]
    [DefaultValue(SearchControlLayout.Horizontal)]
    [Description("Layout orientation of the control")]
    public SearchControlLayout Layout
    {
        get { return ViewState["Layout"] as SearchControlLayout? ?? SearchControlLayout.Horizontal; }
        set { ViewState["Layout"] = value; }
    }
    
    #endregion
    
    #region Control Creation
    
    protected override void CreateChildControls()
    {
        Controls.Clear();
        
        // Create main container
        var container = new Panel { CssClass = GetContainerCssClass() };
        
        // Create search controls based on layout
        if (Layout == SearchControlLayout.Horizontal)
        {
            CreateHorizontalLayout(container);
        }
        else
        {
            CreateVerticalLayout(container);
        }
        
        Controls.Add(container);
    }
    
    private void CreateHorizontalLayout(Panel container)
    {
        // Search type dropdown
        if (SearchTypes.Any())
        {
            _searchTypeDropDown = new DropDownList
            {
                ID = "SearchType",
                CssClass = "form-control search-type-dropdown"
            };
            PopulateSearchTypes();
            container.Controls.Add(_searchTypeDropDown);
        }
        
        // Search text box
        _searchTextBox = new TextBox
        {
            ID = "SearchText",
            CssClass = "form-control search-textbox",
            MaxLength = 255
        };
        _searchTextBox.Attributes["placeholder"] = PlaceholderText;
        _searchTextBox.TextChanged += SearchTextBox_TextChanged;
        _searchTextBox.AutoPostBack = false; // We'll handle this with AJAX
        container.Controls.Add(_searchTextBox);
        
        // Search button
        _searchButton = new Button
        {
            ID = "SearchButton",
            Text = "Search",
            CssClass = "btn btn-primary search-button"
        };
        _searchButton.Click += SearchButton_Click;
        container.Controls.Add(_searchButton);
        
        // Clear button
        _clearButton = new Button
        {
            ID = "ClearButton",
            Text = "Clear",
            CssClass = "btn btn-outline-secondary clear-button"
        };
        _clearButton.Click += ClearButton_Click;
        _clearButton.CausesValidation = false;
        container.Controls.Add(_clearButton);
        
        // Suggestions panel (hidden by default)
        if (EnableAutoSuggest)
        {
            CreateSuggestionsPanel(container);
        }
    }
    
    private void CreateVerticalLayout(Panel container)
    {
        // Search type dropdown row
        if (SearchTypes.Any())
        {
            var typeRow = new Panel { CssClass = "search-row" };
            var typeLabel = new Label { Text = "Search Type:", CssClass = "search-label" };
            
            _searchTypeDropDown = new DropDownList
            {
                ID = "SearchType",
                CssClass = "form-control"
            };
            PopulateSearchTypes();
            
            typeRow.Controls.Add(typeLabel);
            typeRow.Controls.Add(_searchTypeDropDown);
            container.Controls.Add(typeRow);
        }
        
        // Search text row
        var textRow = new Panel { CssClass = "search-row" };
        var textLabel = new Label { Text = "Search Terms:", CssClass = "search-label" };
        
        _searchTextBox = new TextBox
        {
            ID = "SearchText",
            CssClass = "form-control",
            MaxLength = 255
        };
        _searchTextBox.Attributes["placeholder"] = PlaceholderText;
        _searchTextBox.TextChanged += SearchTextBox_TextChanged;
        
        textRow.Controls.Add(textLabel);
        textRow.Controls.Add(_searchTextBox);
        container.Controls.Add(textRow);
        
        // Buttons row
        var buttonRow = new Panel { CssClass = "search-row search-buttons" };
        
        _searchButton = new Button
        {
            ID = "SearchButton",
            Text = "Search",
            CssClass = "btn btn-primary"
        };
        _searchButton.Click += SearchButton_Click;
        
        _clearButton = new Button
        {
            ID = "ClearButton",
            Text = "Clear",
            CssClass = "btn btn-outline-secondary"
        };
        _clearButton.Click += ClearButton_Click;
        _clearButton.CausesValidation = false;
        
        buttonRow.Controls.Add(_searchButton);
        buttonRow.Controls.Add(_clearButton);
        container.Controls.Add(buttonRow);
        
        // Suggestions panel
        if (EnableAutoSuggest)
        {
            CreateSuggestionsPanel(container);
        }
    }
    
    private void CreateSuggestionsPanel(Panel container)
    {
        _suggestionsPanel = new Panel
        {
            ID = "SuggestionsPanel",
            CssClass = "search-suggestions",
            Visible = false
        };
        
        // UpdatePanel for AJAX suggestions
        _updatePanel = new UpdatePanel
        {
            ID = "SuggestionsUpdatePanel",
            UpdateMode = UpdatePanelUpdateMode.Conditional
        };
        _updatePanel.ContentTemplate = new SuggestionsTemplate(this);
        
        // Timer for delayed search
        _searchTimer = new Timer
        {
            ID = "SearchTimer",
            Interval = AutoSuggestDelay,
            Enabled = false
        };
        _searchTimer.Tick += SearchTimer_Tick;
        
        _suggestionsPanel.Controls.Add(_updatePanel);
        _suggestionsPanel.Controls.Add(_searchTimer);
        container.Controls.Add(_suggestionsPanel);
    }
    
    #endregion
    
    #region Event Handlers
    
    protected void SearchTextBox_TextChanged(object sender, EventArgs e)
    {
        if (EnableAutoSuggest && _searchTextBox.Text.Length >= MinimumPrefixLength)
        {
            // Start the timer for delayed search
            _searchTimer.Enabled = false;
            _searchTimer.Enabled = true;
        }
        else if (_searchTextBox.Text.Length < MinimumPrefixLength)
        {
            // Hide suggestions
            _suggestionsPanel.Visible = false;
        }
        
        OnSearchTextChanged(new SearchEventArgs(_searchTextBox.Text, SelectedSearchType));
    }
    
    protected void SearchButton_Click(object sender, EventArgs e)
    {
        PerformSearch();
    }
    
    protected void ClearButton_Click(object sender, EventArgs e)
    {
        _searchTextBox.Text = string.Empty;
        if (_searchTypeDropDown != null)
        {
            _searchTypeDropDown.SelectedIndex = 0;
        }
        _suggestionsPanel.Visible = false;
        
        OnClearSearch();
    }
    
    protected void SearchTimer_Tick(object sender, EventArgs e)
    {
        _searchTimer.Enabled = false;
        
        if (_searchTextBox.Text.Length >= MinimumPrefixLength)
        {
            // Trigger auto-suggest
            ShowSuggestions();
        }
    }
    
    #endregion
    
    #region Public Methods
    
    public void PerformSearch()
    {
        var searchArgs = new SearchEventArgs(_searchTextBox.Text, SelectedSearchType);
        OnSearch(searchArgs);
        
        // Hide suggestions after search
        if (_suggestionsPanel != null)
        {
            _suggestionsPanel.Visible = false;
        }
    }
    
    public void ClearSearch()
    {
        ClearButton_Click(null, EventArgs.Empty);
    }
    
    public void SetFocus()
    {
        EnsureChildControls();
        _searchTextBox.Focus();
    }
    
    #endregion
    
    #region Private Methods
    
    private string GetContainerCssClass()
    {
        var cssClass = "enterprise-search-control";
        
        switch (Layout)
        {
            case SearchControlLayout.Horizontal:
                cssClass += " horizontal-layout";
                break;
            case SearchControlLayout.Vertical:
                cssClass += " vertical-layout";
                break;
        }
        
        return cssClass;
    }
    
    private void PopulateSearchTypes()
    {
        if (_searchTypeDropDown == null) return;
        
        _searchTypeDropDown.Items.Clear();
        
        if (SearchTypes.Any())
        {
            _searchTypeDropDown.Items.Add(new ListItem("All Types", ""));
            
            foreach (var searchType in SearchTypes)
            {
                _searchTypeDropDown.Items.Add(new ListItem(searchType.DisplayName, searchType.Value));
            }
        }
    }
    
    private void ShowSuggestions()
    {
        // This would typically call a service to get suggestions
        // For demo purposes, we'll show a simple implementation
        
        var suggestions = GetSearchSuggestions(_searchTextBox.Text);
        
        if (suggestions.Any())
        {
            PopulateSuggestions(suggestions);
            _suggestionsPanel.Visible = true;
            _updatePanel.Update();
        }
        else
        {
            _suggestionsPanel.Visible = false;
        }
    }
    
    private List<string> GetSearchSuggestions(string searchText)
    {
        // Mock implementation - in real application, this would call a service
        var mockSuggestions = new List<string>
        {
            "Customer Management",
            "Customer Reports", 
            "Customer Analytics",
            "Order Management",
            "Order History",
            "Product Catalog",
            "Product Reviews"
        };
        
        return mockSuggestions
            .Where(s => s.Contains(searchText, StringComparison.OrdinalIgnoreCase))
            .Take(5)
            .ToList();
    }
    
    private void PopulateSuggestions(List<string> suggestions)
    {
        // Clear existing suggestions
        var suggestionsList = _updatePanel.FindControl("SuggestionsList") as Panel;
        if (suggestionsList != null)
        {
            suggestionsList.Controls.Clear();
            
            foreach (var suggestion in suggestions)
            {
                var suggestionLink = new LinkButton
                {
                    Text = suggestion,
                    CssClass = "suggestion-item",
                    CommandArgument = suggestion
                };
                suggestionLink.Click += SuggestionLink_Click;
                
                suggestionsList.Controls.Add(suggestionLink);
            }
        }
    }
    
    private void SuggestionLink_Click(object sender, EventArgs e)
    {
        var linkButton = sender as LinkButton;
        if (linkButton != null)
        {
            _searchTextBox.Text = linkButton.CommandArgument;
            _suggestionsPanel.Visible = false;
            PerformSearch();
        }
    }
    
    #endregion
    
    #region Event Methods
    
    protected virtual void OnSearch(SearchEventArgs e)
    {
        Search?.Invoke(this, e);
    }
    
    protected virtual void OnSearchTextChanged(SearchEventArgs e)
    {
        SearchTextChanged?.Invoke(this, e);
    }
    
    protected virtual void OnClearSearch()
    {
        ClearSearch?.Invoke(this, EventArgs.Empty);
    }
    
    #endregion
    
    #region Client Script
    
    protected override void OnPreRender(EventArgs e)
    {
        base.OnPreRender(e);
        
        // Register client scripts
        RegisterClientScripts();
    }
    
    private void RegisterClientScripts()
    {
        var script = $@"
            function initializeSearchControl(clientId) {{
                var searchBox = document.getElementById(clientId + '_SearchText');
                var suggestionsPanel = document.getElementById(clientId + '_SuggestionsPanel');
                
                // Handle keyboard navigation in suggestions
                searchBox.addEventListener('keydown', function(e) {{
                    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {{
                        e.preventDefault();
                        navigateSuggestions(e.key === 'ArrowDown');
                    }} else if (e.key === 'Enter') {{
                        var selected = suggestionsPanel.querySelector('.suggestion-selected');
                        if (selected) {{
                            selected.click();
                        }}
                    }} else if (e.key === 'Escape') {{
                        hideSuggestions();
                    }}
                }});
                
                // Hide suggestions when clicking outside
                document.addEventListener('click', function(e) {{
                    if (!searchBox.contains(e.target) && !suggestionsPanel.contains(e.target)) {{
                        hideSuggestions();
                    }}
                }});
            }}
            
            function navigateSuggestions(down) {{
                var suggestions = document.querySelectorAll('.suggestion-item');
                var selected = document.querySelector('.suggestion-selected');
                var currentIndex = -1;
                
                if (selected) {{
                    for (var i = 0; i < suggestions.length; i++) {{
                        if (suggestions[i] === selected) {{
                            currentIndex = i;
                            break;
                        }}
                    }}
                    selected.classList.remove('suggestion-selected');
                }}
                
                if (down) {{
                    currentIndex = Math.min(currentIndex + 1, suggestions.length - 1);
                }} else {{
                    currentIndex = Math.max(currentIndex - 1, 0);
                }}
                
                if (suggestions[currentIndex]) {{
                    suggestions[currentIndex].classList.add('suggestion-selected');
                }}
            }}
            
            function hideSuggestions() {{
                var suggestionsPanel = document.querySelector('.search-suggestions');
                if (suggestionsPanel) {{
                    suggestionsPanel.style.display = 'none';
                }}
            }}
            
            // Initialize when page loads
            document.addEventListener('DOMContentLoaded', function() {{
                initializeSearchControl('{ClientID}');
            }});
        ";
        
        Page.ClientScript.RegisterStartupScript(
            this.GetType(), 
            "SearchControlScript_" + ClientID, 
            script, 
            true);
    }
    
    #endregion
}

#region Supporting Classes

public class SearchEventArgs : EventArgs
{
    public string SearchText { get; }
    public string SearchType { get; }
    
    public SearchEventArgs(string searchText, string searchType)
    {
        SearchText = searchText;
        SearchType = searchType;
    }
}

public class SearchType
{
    public string Value { get; set; }
    public string DisplayName { get; set; }
}

public enum SearchControlLayout
{
    Horizontal,
    Vertical
}

// Template for suggestions panel
public class SuggestionsTemplate : ITemplate
{
    private EnterpriseSearchControl _parentControl;
    
    public SuggestionsTemplate(EnterpriseSearchControl parentControl)
    {
        _parentControl = parentControl;
    }
    
    public void InstantiateIn(Control container)
    {
        var suggestionsList = new Panel
        {
            ID = "SuggestionsList",
            CssClass = "suggestions-list"
        };
        
        container.Controls.Add(suggestionsList);
    }
}

#endregion
```

## 3. Data-Bound Custom Control

### 3.1 Enterprise Data Grid Control

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Web.UI;
using System.Web.UI.WebControls;

[DefaultProperty("DataSourceID")]
[ToolboxData("<{0}:EnterpriseDataGrid runat=server></{0}:EnterpriseDataGrid>")]
[ParseChildren(true)]
[PersistChildren(false)]
public class EnterpriseDataGrid : CompositeDataBoundControl, INamingContainer
{
    #region Fields
    
    private Table _table;
    private TableHeaderRow _headerRow;
    private TableFooterRow _footerRow;
    private Panel _pagerPanel;
    
    #endregion
    
    #region Templates
    
    [Browsable(false)]
    [PersistenceMode(PersistenceMode.InnerProperty)]
    [TemplateContainer(typeof(DataGridItem))]
    public ITemplate HeaderTemplate { get; set; }
    
    [Browsable(false)]
    [PersistenceMode(PersistenceMode.InnerProperty)]
    [TemplateContainer(typeof(DataGridItem))]
    public ITemplate ItemTemplate { get; set; }
    
    [Browsable(false)]
    [PersistenceMode(PersistenceMode.InnerProperty)]
    [TemplateContainer(typeof(DataGridItem))]
    public ITemplate AlternatingItemTemplate { get; set; }
    
    [Browsable(false)]
    [PersistenceMode(PersistenceMode.InnerProperty)]
    [TemplateContainer(typeof(DataGridItem))]
    public ITemplate FooterTemplate { get; set; }
    
    [Browsable(false)]
    [PersistenceMode(PersistenceMode.InnerProperty)]
    [TemplateContainer(typeof(DataGridItem))]
    public ITemplate EmptyDataTemplate { get; set; }
    
    #endregion
    
    #region Properties
    
    [Bindable(true)]
    [Category("Data")]
    [Description("Column definitions")]
    public List<DataGridColumn> Columns
    {
        get { return ViewState["Columns"] as List<DataGridColumn> ?? new List<DataGridColumn>(); }
        set { ViewState["Columns"] = value; }
    }
    
    [Bindable(true)]
    [Category("Paging")]
    [DefaultValue(true)]
    public bool AllowPaging
    {
        get { return ViewState["AllowPaging"] as bool? ?? true; }
        set { ViewState["AllowPaging"] = value; }
    }
    
    [Bindable(true)]
    [Category("Paging")]
    [DefaultValue(10)]
    public int PageSize
    {
        get { return ViewState["PageSize"] as int? ?? 10; }
        set { ViewState["PageSize"] = value; }
    }
    
    [Bindable(true)]
    [Category("Paging")]
    [DefaultValue(0)]
    public int PageIndex
    {
        get { return ViewState["PageIndex"] as int? ?? 0; }
        set { ViewState["PageIndex"] = Math.Max(0, value); }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(true)]
    public bool AllowSorting
    {
        get { return ViewState["AllowSorting"] as bool? ?? true; }
        set { ViewState["AllowSorting"] = value; }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue("")]
    public string SortExpression
    {
        get { return ViewState["SortExpression"] as string ?? string.Empty; }
        set { ViewState["SortExpression"] = value; }
    }
    
    [Bindable(true)]
    [Category("Behavior")]
    [DefaultValue(SortDirection.Ascending)]
    public SortDirection SortDirection
    {
        get { return ViewState["SortDirection"] as SortDirection? ?? SortDirection.Ascending; }
        set { ViewState["SortDirection"] = value; }
    }
    
    [Bindable(true)]
    [Category("Appearance")]
    [DefaultValue("table table-striped table-hover")]
    public string CssClass
    {
        get { return ViewState["CssClass"] as string ?? "table table-striped table-hover"; }
        set { ViewState["CssClass"] = value; }
    }
    
    [Bindable(true)]
    [Category("Appearance")]
    [DefaultValue("No data available.")]
    public string EmptyDataText
    {
        get { return ViewState["EmptyDataText"] as string ?? "No data available."; }
        set { ViewState["EmptyDataText"] = value; }
    }
    
    public int VirtualItemCount
    {
        get { return ViewState["VirtualItemCount"] as int? ?? 0; }
        set { ViewState["VirtualItemCount"] = value; }
    }
    
    #endregion
    
    #region Events
    
    public event EventHandler<DataGridPageEventArgs> PageIndexChanging;
    public event EventHandler<DataGridSortEventArgs> Sorting;
    public event EventHandler<DataGridCommandEventArgs> ItemCommand;
    public event EventHandler<DataGridItemEventArgs> ItemCreated;
    public event EventHandler<DataGridItemEventArgs> ItemDataBound;
    
    #endregion
    
    #region Control Creation
    
    protected override int CreateChildControls(IEnumerable dataSource, bool dataBinding)
    {
        Controls.Clear();
        
        // Create main table
        _table = new Table { CssClass = this.CssClass };
        
        var itemCount = 0;
        
        if (dataBinding)
        {
            // Create header
            CreateHeader();
            
            // Create data rows
            if (dataSource != null)
            {
                itemCount = CreateDataRows(dataSource);
            }
            
            // Create footer
            CreateFooter();
            
            // Create pager
            if (AllowPaging && itemCount > 0)
            {
                CreatePager();
            }
            
            // Handle empty data
            if (itemCount == 0)
            {
                CreateEmptyDataRow();
            }
        }
        
        Controls.Add(_table);
        
        if (_pagerPanel != null)
        {
            Controls.Add(_pagerPanel);
        }
        
        return itemCount;
    }
    
    private void CreateHeader()
    {
        if (HeaderTemplate != null || Columns.Any())
        {
            _headerRow = new TableHeaderRow();
            
            if (HeaderTemplate != null)
            {
                var headerItem = new DataGridItem(0, ListItemType.Header);
                HeaderTemplate.InstantiateIn(headerItem);
                OnItemCreated(new DataGridItemEventArgs(headerItem));
                
                var headerCell = new TableHeaderCell();
                headerCell.Controls.Add(headerItem);
                headerCell.ColumnSpan = Math.Max(1, Columns.Count);
                _headerRow.Cells.Add(headerCell);
            }
            else
            {
                foreach (var column in Columns)
                {
                    var headerCell = new TableHeaderCell
                    {
                        Text = column.HeaderText
                    };
                    
                    if (AllowSorting && !string.IsNullOrEmpty(column.SortExpression))
                    {
                        var sortLink = new LinkButton
                        {
                            Text = column.HeaderText,
                            CommandName = "Sort",
                            CommandArgument = column.SortExpression
                        };
                        sortLink.Command += SortCommand;
                        
                        headerCell.Controls.Clear();
                        headerCell.Controls.Add(sortLink);
                        
                        // Add sort indicator
                        if (SortExpression == column.SortExpression)
                        {
                            var indicator = new Literal
                            {
                                Text = SortDirection == SortDirection.Ascending ? " ▲" : " ▼"
                            };
                            headerCell.Controls.Add(indicator);
                        }
                    }
                    
                    _headerRow.Cells.Add(headerCell);
                }
            }
            
            _table.Rows.Add(_headerRow);
        }
    }
    
    private int CreateDataRows(IEnumerable dataSource)
    {
        var itemIndex = 0;
        
        foreach (var dataItem in dataSource)
        {
            var itemType = itemIndex % 2 == 0 ? ListItemType.Item : ListItemType.AlternatingItem;
            var gridItem = new DataGridItem(itemIndex, itemType);
            
            // Use appropriate template
            var template = itemType == ListItemType.AlternatingItem && AlternatingItemTemplate != null
                ? AlternatingItemTemplate
                : ItemTemplate;
                
            if (template != null)
            {
                template.InstantiateIn(gridItem);
            }
            else
            {
                // Auto-generate cells based on columns
                CreateAutoCells(gridItem, dataItem);
            }
            
            // Set data item
            gridItem.DataItem = dataItem;
            
            // Raise events
            OnItemCreated(new DataGridItemEventArgs(gridItem));
            gridItem.DataBind();
            OnItemDataBound(new DataGridItemEventArgs(gridItem));
            
            // Create table row
            var tableRow = new TableRow();
            var tableCell = new TableCell();
            tableCell.Controls.Add(gridItem);
            tableRow.Cells.Add(tableCell);
            
            _table.Rows.Add(tableRow);
            itemIndex++;
        }
        
        return itemIndex;
    }
    
    private void CreateAutoCells(DataGridItem gridItem, object dataItem)
    {
        foreach (var column in Columns)
        {
            var cell = new TableCell();
            
            if (!string.IsNullOrEmpty(column.DataField))
            {
                var value = DataBinder.Eval(dataItem, column.DataField);
                
                if (!string.IsNullOrEmpty(column.DataFormatString))
                {
                    cell.Text = string.Format(column.DataFormatString, value);
                }
                else
                {
                    cell.Text = value?.ToString() ?? string.Empty;
                }
            }
            
            gridItem.Cells.Add(cell);
        }
    }
    
    private void CreateFooter()
    {
        if (FooterTemplate != null)
        {
            _footerRow = new TableFooterRow();
            
            var footerItem = new DataGridItem(0, ListItemType.Footer);
            FooterTemplate.InstantiateIn(footerItem);
            OnItemCreated(new DataGridItemEventArgs(footerItem));
            
            var footerCell = new TableCell();
            footerCell.Controls.Add(footerItem);
            footerCell.ColumnSpan = Math.Max(1, Columns.Count);
            _footerRow.Cells.Add(footerCell);
            
            _table.Rows.Add(_footerRow);
        }
    }
    
    private void CreatePager()
    {
        if (!AllowPaging) return;
        
        _pagerPanel = new Panel { CssClass = "data-grid-pager" };
        
        var totalRecords = VirtualItemCount > 0 ? VirtualItemCount : PageSize;
        var totalPages = (int)Math.Ceiling((double)totalRecords / PageSize);
        
        if (totalPages <= 1) return;
        
        // Previous button
        if (PageIndex > 0)
        {
            var prevButton = new LinkButton
            {
                Text = "« Previous",
                CommandName = "Page",
                CommandArgument = (PageIndex - 1).ToString(),
                CssClass = "btn btn-outline-primary btn-sm"
            };
            prevButton.Command += PageCommand;
            _pagerPanel.Controls.Add(prevButton);
            _pagerPanel.Controls.Add(new Literal { Text = " " });
        }
        
        // Page numbers
        var startPage = Math.Max(0, PageIndex - 2);
        var endPage = Math.Min(totalPages - 1, PageIndex + 2);
        
        for (var i = startPage; i <= endPage; i++)
        {
            if (i == PageIndex)
            {
                var currentPage = new Label
                {
                    Text = (i + 1).ToString(),
                    CssClass = "btn btn-primary btn-sm"
                };
                _pagerPanel.Controls.Add(currentPage);
            }
            else
            {
                var pageButton = new LinkButton
                {
                    Text = (i + 1).ToString(),
                    CommandName = "Page",
                    CommandArgument = i.ToString(),
                    CssClass = "btn btn-outline-primary btn-sm"
                };
                pageButton.Command += PageCommand;
                _pagerPanel.Controls.Add(pageButton);
            }
            
            _pagerPanel.Controls.Add(new Literal { Text = " " });
        }
        
        // Next button
        if (PageIndex < totalPages - 1)
        {
            var nextButton = new LinkButton
            {
                Text = "Next »",
                CommandName = "Page",
                CommandArgument = (PageIndex + 1).ToString(),
                CssClass = "btn btn-outline-primary btn-sm"
            };
            nextButton.Command += PageCommand;
            _pagerPanel.Controls.Add(nextButton);
        }
    }
    
    private void CreateEmptyDataRow()
    {
        var emptyRow = new TableRow();
        var emptyCell = new TableCell
        {
            ColumnSpan = Math.Max(1, Columns.Count),
            CssClass = "empty-data-cell"
        };
        
        if (EmptyDataTemplate != null)
        {
            var emptyItem = new DataGridItem(0, ListItemType.Item);
            EmptyDataTemplate.InstantiateIn(emptyItem);
            emptyCell.Controls.Add(emptyItem);
        }
        else
        {
            emptyCell.Text = EmptyDataText;
        }
        
        emptyRow.Cells.Add(emptyCell);
        _table.Rows.Add(emptyRow);
    }
    
    #endregion
    
    #region Event Handlers
    
    private void PageCommand(object sender, CommandEventArgs e)
    {
        var newPageIndex = Convert.ToInt32(e.CommandArgument);
        OnPageIndexChanging(new DataGridPageEventArgs(newPageIndex));
    }
    
    private void SortCommand(object sender, CommandEventArgs e)
    {
        var sortExpression = e.CommandArgument.ToString();
        var newSortDirection = SortDirection;
        
        if (SortExpression == sortExpression)
        {
            newSortDirection = SortDirection == SortDirection.Ascending 
                ? SortDirection.Descending 
                : SortDirection.Ascending;
        }
        else
        {
            newSortDirection = SortDirection.Ascending;
        }
        
        OnSorting(new DataGridSortEventArgs(sortExpression, newSortDirection));
    }
    
    #endregion
    
    #region Event Methods
    
    protected virtual void OnPageIndexChanging(DataGridPageEventArgs e)
    {
        PageIndexChanging?.Invoke(this, e);
    }
    
    protected virtual void OnSorting(DataGridSortEventArgs e)
    {
        Sorting?.Invoke(this, e);
    }
    
    protected virtual void OnItemCommand(DataGridCommandEventArgs e)
    {
        ItemCommand?.Invoke(this, e);
    }
    
    protected virtual void OnItemCreated(DataGridItemEventArgs e)
    {
        ItemCreated?.Invoke(this, e);
    }
    
    protected virtual void OnItemDataBound(DataGridItemEventArgs e)
    {
        ItemDataBound?.Invoke(this, e);
    }
    
    #endregion
}

#region Supporting Classes

public class DataGridItem : Control, INamingContainer
{
    public int ItemIndex { get; }
    public ListItemType ItemType { get; }
    public object DataItem { get; set; }
    public TableCellCollection Cells { get; }
    
    public DataGridItem(int itemIndex, ListItemType itemType)
    {
        ItemIndex = itemIndex;
        ItemType = itemType;
        Cells = new TableCellCollection(new TableRow());
    }
}

public class DataGridColumn
{
    public string HeaderText { get; set; }
    public string DataField { get; set; }
    public string SortExpression { get; set; }
    public string DataFormatString { get; set; }
    public bool ReadOnly { get; set; }
}

public class DataGridPageEventArgs : EventArgs
{
    public int NewPageIndex { get; }
    
    public DataGridPageEventArgs(int newPageIndex)
    {
        NewPageIndex = newPageIndex;
    }
}

public class DataGridSortEventArgs : EventArgs
{
    public string SortExpression { get; }
    public SortDirection SortDirection { get; }
    
    public DataGridSortEventArgs(string sortExpression, SortDirection sortDirection)
    {
        SortExpression = sortExpression;
        SortDirection = sortDirection;
    }
}

public class DataGridCommandEventArgs : EventArgs
{
    public string CommandName { get; }
    public object CommandArgument { get; }
    public DataGridItem Item { get; }
    
    public DataGridCommandEventArgs(string commandName, object commandArgument, DataGridItem item)
    {
        CommandName = commandName;
        CommandArgument = commandArgument;
        Item = item;
    }
}

public class DataGridItemEventArgs : EventArgs
{
    public DataGridItem Item { get; }
    
    public DataGridItemEventArgs(DataGridItem item)
    {
        Item = item;
    }
}

#endregion
```

## 4. Migration to Modern Web Components

### 4.1 Modern Web Component Target

```typescript
// Modern Web Component using Lit Element
import { LitElement, html, css, property } from 'lit-element';

interface SearchResult {
  id: string;
  title: string;
  description: string;
  type: string;
}

interface SearchOptions {
  searchType?: string;
  enableAutoSuggest?: boolean;
  minPrefixLength?: number;
  autoSuggestDelay?: number;
}

export class EnterpriseSearchComponent extends LitElement {
  @property({ type: String })
  searchText = '';
  
  @property({ type: String })
  selectedSearchType = '';
  
  @property({ type: Boolean })
  enableAutoSuggest = true;
  
  @property({ type: Number })
  minPrefixLength = 3;
  
  @property({ type: Number })
  autoSuggestDelay = 500;
  
  @property({ type: Array })
  searchTypes: { value: string; displayName: string }[] = [];
  
  @property({ type: Array })
  suggestions: SearchResult[] = [];
  
  @property({ type: Boolean })
  showSuggestions = false;
  
  @property({ type: Boolean })
  isSearching = false;
  
  private searchTimer?: number;
  
  static styles = css`
    :host {
      display: block;
      font-family: system-ui, sans-serif;
    }
    
    .search-container {
      display: flex;
      gap: 0.5rem;
      align-items: center;
      position: relative;
    }
    
    .search-input {
      flex: 1;
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 1rem;
    }
    
    .search-type-select {
      padding: 0.5rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      background: white;
    }
    
    .search-button, .clear-button {
      padding: 0.5rem 1rem;
      border: 1px solid #007bff;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
    }
    
    .search-button {
      background: #007bff;
      color: white;
    }
    
    .clear-button {
      background: white;
      color: #007bff;
    }
    
    .suggestions-panel {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      border: 1px solid #ccc;
      border-top: none;
      border-radius: 0 0 4px 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      z-index: 1000;
      max-height: 200px;
      overflow-y: auto;
    }
    
    .suggestion-item {
      padding: 0.5rem;
      cursor: pointer;
      border-bottom: 1px solid #eee;
    }
    
    .suggestion-item:hover,
    .suggestion-item.selected {
      background: #f8f9fa;
    }
    
    .suggestion-item:last-child {
      border-bottom: none;
    }
    
    .loading {
      padding: 0.5rem;
      text-align: center;
      color: #666;
    }
  `;
  
  render() {
    return html`
      <div class="search-container">
        ${this.searchTypes.length > 0 ? html`
          <select 
            class="search-type-select"
            .value=${this.selectedSearchType}
            @change=${this.handleSearchTypeChange}
          >
            <option value="">All Types</option>
            ${this.searchTypes.map(type => html`
              <option value=${type.value}>${type.displayName}</option>
            `)}
          </select>
        ` : ''}
        
        <input
          class="search-input"
          type="text"
          placeholder="Search..."
          .value=${this.searchText}
          @input=${this.handleSearchInput}
          @keydown=${this.handleKeyDown}
          @focus=${this.handleFocus}
        />
        
        <button 
          class="search-button"
          @click=${this.handleSearch}
          ?disabled=${this.isSearching}
        >
          ${this.isSearching ? 'Searching...' : 'Search'}
        </button>
        
        <button 
          class="clear-button"
          @click=${this.handleClear}
        >
          Clear
        </button>
        
        ${this.showSuggestions ? html`
          <div class="suggestions-panel">
            ${this.suggestions.length > 0 ? 
              this.suggestions.map((suggestion, index) => html`
                <div 
                  class="suggestion-item"
                  data-index=${index}
                  @click=${() => this.selectSuggestion(suggestion)}
                >
                  <strong>${suggestion.title}</strong>
                  ${suggestion.description ? html`<br><small>${suggestion.description}</small>` : ''}
                </div>
              `) :
              html`<div class="loading">No suggestions found</div>`
            }
          </div>
        ` : ''}
      </div>
    `;
  }
  
  private handleSearchInput(e: Event) {
    const target = e.target as HTMLInputElement;
    this.searchText = target.value;
    
    // Dispatch search text changed event
    this.dispatchEvent(new CustomEvent('searchTextChanged', {
      detail: { searchText: this.searchText, searchType: this.selectedSearchType }
    }));
    
    // Handle auto-suggest
    if (this.enableAutoSuggest && this.searchText.length >= this.minPrefixLength) {
      this.startAutoSuggest();
    } else {
      this.hideSuggestions();
    }
  }
  
  private handleSearchTypeChange(e: Event) {
    const target = e.target as HTMLSelectElement;
    this.selectedSearchType = target.value;
  }
  
  private handleSearch() {
    this.performSearch();
  }
  
  private handleClear() {
    this.searchText = '';
    this.selectedSearchType = '';
    this.hideSuggestions();
    
    this.dispatchEvent(new CustomEvent('clearSearch'));
  }
  
  private handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      this.performSearch();
    } else if (e.key === 'Escape') {
      this.hideSuggestions();
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      this.navigateSuggestions(e.key === 'ArrowDown');
    }
  }
  
  private handleFocus() {
    if (this.suggestions.length > 0 && this.searchText.length >= this.minPrefixLength) {
      this.showSuggestions = true;
    }
  }
  
  private startAutoSuggest() {
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
    
    this.searchTimer = window.setTimeout(() => {
      this.getSuggestions();
    }, this.autoSuggestDelay);
  }
  
  private async getSuggestions() {
    try {
      // Mock API call - replace with actual service
      const response = await fetch(`/api/search/suggestions?q=${encodeURIComponent(this.searchText)}&type=${this.selectedSearchType}`);
      const suggestions = await response.json();
      
      this.suggestions = suggestions;
      this.showSuggestions = suggestions.length > 0;
    } catch (error) {
      console.error('Failed to get suggestions:', error);
      this.suggestions = [];
      this.showSuggestions = false;
    }
  }
  
  private performSearch() {
    this.hideSuggestions();
    this.isSearching = true;
    
    this.dispatchEvent(new CustomEvent('search', {
      detail: { 
        searchText: this.searchText, 
        searchType: this.selectedSearchType 
      }
    }));
    
    // Reset searching state after a brief delay
    setTimeout(() => {
      this.isSearching = false;
    }, 500);
  }
  
  private selectSuggestion(suggestion: SearchResult) {
    this.searchText = suggestion.title;
    this.hideSuggestions();
    this.performSearch();
  }
  
  private navigateSuggestions(down: boolean) {
    const items = this.shadowRoot?.querySelectorAll('.suggestion-item');
    if (!items || items.length === 0) return;
    
    const selected = this.shadowRoot?.querySelector('.suggestion-item.selected');
    let currentIndex = -1;
    
    if (selected) {
      currentIndex = parseInt((selected as HTMLElement).dataset.index || '-1');
      selected.classList.remove('selected');
    }
    
    if (down) {
      currentIndex = Math.min(currentIndex + 1, items.length - 1);
    } else {
      currentIndex = Math.max(currentIndex - 1, 0);
    }
    
    items[currentIndex].classList.add('selected');
    items[currentIndex].scrollIntoView({ block: 'nearest' });
  }
  
  private hideSuggestions() {
    this.showSuggestions = false;
    this.suggestions = [];
    
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
  }
}

// Register the custom element
customElements.define('enterprise-search', EnterpriseSearchComponent);
```

### 4.2 Migration Strategy Pattern

```csharp
// Transitional wrapper for gradual migration
public class ModernControlWrapper : Control
{
    public string ControlType { get; set; }
    public Dictionary<string, object> Properties { get; set; } = new Dictionary<string, object>();
    
    protected override void Render(HtmlTextWriter writer)
    {
        // Render modern web component
        writer.AddAttribute("is", ControlType);
        
        foreach (var prop in Properties)
        {
            writer.AddAttribute(ConvertPropertyName(prop.Key), prop.Value.ToString());
        }
        
        writer.RenderBeginTag("div");
        writer.RenderEndTag();
        
        // Add polyfill script for older browsers
        if (!Page.ClientScript.IsClientScriptIncludeRegistered("WebComponentsPolyfill"))
        {
            Page.ClientScript.RegisterClientScriptInclude(
                "WebComponentsPolyfill",
                "https://unpkg.com/@webcomponents/webcomponentsjs@^2/webcomponents-bundle.js");
        }
    }
    
    private string ConvertPropertyName(string propName)
    {
        // Convert PascalCase to kebab-case
        return string.Concat(propName.Select((x, i) => i > 0 && char.IsUpper(x) ? "-" + x.ToString() : x.ToString())).ToLower();
    }
}
```

---

**Custom Controls Analysis Status**: ✅ COMPLETE  
**Pattern Coverage**: ✅ COMPREHENSIVE CUSTOM CONTROL EXAMPLES  
**Migration Strategy**: ✅ MODERN WEB COMPONENT MIGRATION PATTERNS  
**Control Architecture**: ✅ ENTERPRISE-READY IMPLEMENTATIONS

*Code Archaeologist: Custom Server Control Patterns Analysis Complete*  
*Memory Key: hive/analysis/patterns/webforms-custom-controls*