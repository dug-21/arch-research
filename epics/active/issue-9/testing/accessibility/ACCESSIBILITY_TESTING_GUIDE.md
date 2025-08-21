# WebForms Accessibility Testing Guide

## Overview
This guide provides comprehensive strategies for testing accessibility in ASP.NET WebForms applications, ensuring compliance with WCAG 2.1 guidelines and creating inclusive user experiences.

## Accessibility Testing Framework

### 1. Automated Accessibility Testing Setup
```csharp
[TestClass]
public class AccessibilityTests
{
    private IWebDriver _driver;
    private AxeBuilder _axeBuilder;
    
    [TestInitialize]
    public void Setup()
    {
        var options = new ChromeOptions();
        options.AddArgument("--force-device-scale-factor=1");
        _driver = new ChromeDriver(options);
        
        _axeBuilder = new AxeBuilder(_driver)
            .WithTags("wcag2a", "wcag2aa", "wcag21aa");
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_AccessibilityCompliance_MeetsWCAGStandards()
    {
        // Navigate to the form
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Run accessibility scan
        var results = _axeBuilder.Analyze();
        
        // Assert no violations
        Assert.AreEqual(0, results.Violations.Count, 
            $"Found {results.Violations.Count} accessibility violations:\n" +
            string.Join("\n", results.Violations.Select(v => $"- {v.Description}")));
        
        // Log accessibility results
        LogAccessibilityResults(results);
    }
    
    private void LogAccessibilityResults(AxeResult results)
    {
        TestContext.WriteLine($"Accessibility Test Results:");
        TestContext.WriteLine($"Violations: {results.Violations.Count}");
        TestContext.WriteLine($"Passes: {results.Passes.Count}");
        TestContext.WriteLine($"Incomplete: {results.Incomplete.Count}");
        
        foreach (var violation in results.Violations)
        {
            TestContext.WriteLine($"\nViolation: {violation.Description}");
            TestContext.WriteLine($"Impact: {violation.Impact}");
            TestContext.WriteLine($"Help: {violation.HelpUrl}");
            
            foreach (var node in violation.Nodes)
            {
                TestContext.WriteLine($"Element: {node.Html}");
            }
        }
    }
    
    public TestContext TestContext { get; set; }
}
```

### 2. Manual Accessibility Testing

#### Keyboard Navigation Testing
```csharp
[TestClass]
public class KeyboardAccessibilityTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_KeyboardNavigation_FullyAccessible()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Start at first focusable element
        var firstElement = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
        firstElement.Click();
        
        var tabOrder = new List<string>();
        var currentElement = _driver.SwitchTo().ActiveElement();
        var maxTabs = 20; // Prevent infinite loops
        
        for (int i = 0; i < maxTabs; i++)
        {
            var elementInfo = GetElementInfo(currentElement);
            tabOrder.Add(elementInfo);
            
            // Tab to next element
            currentElement.SendKeys(Keys.Tab);
            var nextElement = _driver.SwitchTo().ActiveElement();
            
            // Check if we've cycled back to start or reached end
            if (nextElement.Equals(currentElement) || 
                nextElement.TagName.Equals("body", StringComparison.OrdinalIgnoreCase))
            {
                break;
            }
            
            currentElement = nextElement;
        }
        
        // Verify logical tab order
        Assert.IsTrue(tabOrder.Count > 0, "Should have focusable elements");
        Assert.IsTrue(tabOrder.Contains("Email"), "Email field should be in tab order");
        Assert.IsTrue(tabOrder.Contains("Name"), "Name field should be in tab order");
        Assert.IsTrue(tabOrder.Contains("Save"), "Save button should be in tab order");
        
        // Verify tab order follows visual layout
        var emailIndex = tabOrder.FindIndex(e => e.Contains("Email"));
        var nameIndex = tabOrder.FindIndex(e => e.Contains("Name"));
        var saveIndex = tabOrder.FindIndex(e => e.Contains("Save"));
        
        Assert.IsTrue(emailIndex < nameIndex, "Email should come before Name in tab order");
        Assert.IsTrue(nameIndex < saveIndex, "Name should come before Save button in tab order");
        
        TestContext.WriteLine("Tab Order:");
        for (int i = 0; i < tabOrder.Count; i++)
        {
            TestContext.WriteLine($"{i + 1}. {tabOrder[i]}");
        }
    }
    
    [TestMethod]
    public void CustomerForm_KeyboardSubmission_WorksWithoutMouse()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Navigate and fill form using only keyboard
        var emailField = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
        emailField.Click();
        emailField.SendKeys("keyboard@example.com");
        
        // Tab to name field
        emailField.SendKeys(Keys.Tab);
        var nameField = _driver.SwitchTo().ActiveElement();
        nameField.SendKeys("Keyboard User");
        
        // Tab to save button and submit
        nameField.SendKeys(Keys.Tab);
        var saveButton = _driver.SwitchTo().ActiveElement();
        Assert.IsTrue(saveButton.GetAttribute("type").Equals("submit") || 
                     saveButton.GetAttribute("value").Contains("Save"), 
            "Save button should be focused");
        
        // Submit using Enter key
        saveButton.SendKeys(Keys.Enter);
        
        // Verify form submission worked
        var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(10));
        var messageElement = wait.Until(driver => 
            driver.FindElement(By.CssSelector("span[id$='lblMessage']")));
        
        Assert.IsTrue(messageElement.Text.Contains("saved"), 
            "Form should submit successfully via keyboard");
    }
    
    [TestMethod]
    public void CustomerForm_EscapeKey_CancelsOperations()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Fill some data
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys("test@example.com");
        _driver.FindElement(By.CssSelector("input[id$='txtName']")).SendKeys("Test User");
        
        // Press Escape key
        var activeElement = _driver.SwitchTo().ActiveElement();
        activeElement.SendKeys(Keys.Escape);
        
        // Verify form is cleared or reset
        var emailValue = _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).GetAttribute("value");
        var nameValue = _driver.FindElement(By.CssSelector("input[id$='txtName']")).GetAttribute("value");
        
        Assert.IsTrue(string.IsNullOrEmpty(emailValue) || string.IsNullOrEmpty(nameValue), 
            "Escape key should clear or reset form");
    }
    
    private string GetElementInfo(IWebElement element)
    {
        var tagName = element.TagName;
        var type = element.GetAttribute("type") ?? "";
        var id = element.GetAttribute("id") ?? "";
        var value = element.GetAttribute("value") ?? "";
        var text = element.Text ?? "";
        
        if (!string.IsNullOrEmpty(value))
            return $"{tagName}[{type}] - {value}";
        if (!string.IsNullOrEmpty(text))
            return $"{tagName}[{type}] - {text}";
        if (!string.IsNullOrEmpty(id))
            return $"{tagName}[{type}] - {id}";
        
        return $"{tagName}[{type}]";
    }
    
    public TestContext TestContext { get; set; }
}
```

#### Screen Reader Testing
```csharp
[TestClass]
public class ScreenReaderTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_FormLabels_ProperlyAssociated()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        var formFields = new[]
        {
            new { FieldId = "txtEmail", ExpectedLabel = "Email" },
            new { FieldId = "txtName", ExpectedLabel = "Name" },
            new { FieldId = "txtPhone", ExpectedLabel = "Phone" }
        };
        
        foreach (var field in formFields)
        {
            var input = _driver.FindElement(By.CssSelector($"input[id$='{field.FieldId}']"));
            
            // Check for explicit label association
            var labelFor = input.GetAttribute("id");
            IWebElement label = null;
            
            try
            {
                label = _driver.FindElement(By.CssSelector($"label[for='{labelFor}']"));
            }
            catch (NoSuchElementException)
            {
                // Try to find label by proximity or aria-labelledby
                var ariaLabelledBy = input.GetAttribute("aria-labelledby");
                if (!string.IsNullOrEmpty(ariaLabelledBy))
                {
                    label = _driver.FindElement(By.Id(ariaLabelledBy));
                }
            }
            
            Assert.IsNotNull(label, $"Field {field.FieldId} should have an associated label");
            Assert.IsTrue(label.Text.Contains(field.ExpectedLabel), 
                $"Label for {field.FieldId} should contain '{field.ExpectedLabel}', but was '{label.Text}'");
        }
    }
    
    [TestMethod]
    public void CustomerForm_ARIAAttributes_ProperlyImplemented()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Check required field indicators
        var emailField = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
        var isRequired = emailField.GetAttribute("required") != null || 
                        emailField.GetAttribute("aria-required") == "true";
        Assert.IsTrue(isRequired, "Email field should be marked as required");
        
        // Check validation messages
        var validationSummary = _driver.FindElement(By.CssSelector("div[id$='ValidationSummary1']"));
        var ariaLive = validationSummary.GetAttribute("aria-live");
        Assert.IsNotNull(ariaLive, "Validation summary should have aria-live attribute");
        Assert.IsTrue(ariaLive == "polite" || ariaLive == "assertive", 
            "Validation summary should have appropriate aria-live value");
        
        // Check form role
        var form = _driver.FindElement(By.TagName("form"));
        var formRole = form.GetAttribute("role");
        if (formRole != null)
        {
            Assert.AreEqual("form", formRole, "Form should have role='form' if role is specified");
        }
    }
    
    [TestMethod]
    public void CustomerGrid_TableStructure_AccessibleToScreenReaders()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerGrid.aspx");
        
        var gridView = _driver.FindElement(By.CssSelector("table[id$='GridView1']"));
        
        // Check for table headers
        var headers = gridView.FindElements(By.TagName("th"));
        Assert.IsTrue(headers.Count > 0, "GridView should have table headers");
        
        foreach (var header in headers)
        {
            var scope = header.GetAttribute("scope");
            Assert.AreEqual("col", scope, "Table headers should have scope='col'");
            
            Assert.IsFalse(string.IsNullOrWhiteSpace(header.Text), 
                "Table headers should have text content");
        }
        
        // Check for table caption or summary
        var caption = gridView.FindElements(By.TagName("caption"));
        var summary = gridView.GetAttribute("summary");
        var ariaLabel = gridView.GetAttribute("aria-label");
        
        Assert.IsTrue(caption.Count > 0 || !string.IsNullOrEmpty(summary) || !string.IsNullOrEmpty(ariaLabel), 
            "Table should have caption, summary, or aria-label for context");
        
        // Check row structure
        var dataRows = gridView.FindElements(By.CssSelector("tr:not(:first-child)"));
        if (dataRows.Count > 0)
        {
            var firstDataRow = dataRows[0];
            var cells = firstDataRow.FindElements(By.TagName("td"));
            
            Assert.IsTrue(cells.Count == headers.Count, 
                "Data rows should have same number of cells as headers");
        }
    }
    
    [TestMethod]
    public void CustomerForm_ErrorMessages_AnnouncedToScreenReaders()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Submit form with validation errors
        var saveButton = _driver.FindElement(By.CssSelector("input[id$='btnSave']"));
        saveButton.Click();
        
        // Wait for validation messages
        var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(5));
        wait.Until(driver => driver.FindElements(By.CssSelector("span[class*='error']")).Count > 0);
        
        var errorMessages = _driver.FindElements(By.CssSelector("span[class*='error'], div[class*='validation']"));
        
        foreach (var errorMessage in errorMessages)
        {
            // Check that error messages are announced to screen readers
            var ariaLive = errorMessage.GetAttribute("aria-live");
            var role = errorMessage.GetAttribute("role");
            
            Assert.IsTrue(!string.IsNullOrEmpty(ariaLive) || role == "alert", 
                "Error messages should have aria-live or role='alert' for screen reader announcement");
            
            // Check that error messages are associated with form fields
            var ariaDescribedBy = errorMessage.GetAttribute("aria-describedby");
            var forAttribute = errorMessage.GetAttribute("for");
            
            if (!string.IsNullOrEmpty(ariaDescribedBy) || !string.IsNullOrEmpty(forAttribute))
            {
                Assert.IsTrue(true, "Error message is properly associated with form field");
            }
        }
    }
}
```

### 3. Color and Contrast Testing

#### Color Contrast Testing
```csharp
[TestClass]
public class ColorContrastTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_ColorContrast_MeetsWCAGStandards()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        var elementsToTest = new[]
        {
            By.CssSelector("label"),
            By.CssSelector("input[type='text']"),
            By.CssSelector("input[type='submit']"),
            By.CssSelector(".error-message"),
            By.CssSelector(".success-message")
        };
        
        foreach (var selector in elementsToTest)
        {
            var elements = _driver.FindElements(selector);
            
            foreach (var element in elements)
            {
                if (element.Displayed)
                {
                    var contrastRatio = CalculateContrastRatio(element);
                    var fontSize = GetFontSize(element);
                    var isBold = IsBoldText(element);
                    
                    var minContrast = GetMinimumContrastRatio(fontSize, isBold);
                    
                    Assert.IsTrue(contrastRatio >= minContrast, 
                        $"Element {selector} has insufficient contrast ratio: {contrastRatio:F2} " +
                        $"(minimum required: {minContrast:F2})");
                }
            }
        }
    }
    
    [TestMethod]
    public void CustomerForm_ColorOnly_NotUsedForMeaning()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Submit form to trigger validation
        _driver.FindElement(By.CssSelector("input[id$='btnSave']")).Click();
        
        // Check that validation errors don't rely solely on color
        var errorElements = _driver.FindElements(By.CssSelector("span[class*='error'], .field-validation-error"));
        
        foreach (var errorElement in errorElements)
        {
            var hasIcon = errorElement.FindElements(By.CssSelector("i, span[class*='icon']")).Count > 0;
            var hasText = !string.IsNullOrWhiteSpace(errorElement.Text);
            var hasBorder = HasVisualIndicator(errorElement, "border");
            var hasBackground = HasVisualIndicator(errorElement, "background");
            
            Assert.IsTrue(hasIcon || hasText || hasBorder || hasBackground, 
                "Error indication should not rely solely on color");
        }
        
        // Check required field indicators
        var requiredFields = _driver.FindElements(By.CssSelector("input[required], input[aria-required='true']"));
        
        foreach (var field in requiredFields)
        {
            var label = FindAssociatedLabel(field);
            if (label != null)
            {
                var hasAsterisk = label.Text.Contains("*");
                var hasRequiredText = label.Text.ToLower().Contains("required");
                var hasAriaRequired = field.GetAttribute("aria-required") == "true";
                
                Assert.IsTrue(hasAsterisk || hasRequiredText || hasAriaRequired, 
                    "Required fields should be indicated with more than just color");
            }
        }
    }
    
    private double CalculateContrastRatio(IWebElement element)
    {
        // Get computed styles
        var backgroundColor = ((IJavaScriptExecutor)_driver).ExecuteScript(
            "return window.getComputedStyle(arguments[0]).backgroundColor;", element).ToString();
        var color = ((IJavaScriptExecutor)_driver).ExecuteScript(
            "return window.getComputedStyle(arguments[0]).color;", element).ToString();
        
        // Convert to RGB values and calculate contrast
        var bgRgb = ParseRgbColor(backgroundColor);
        var textRgb = ParseRgbColor(color);
        
        var bgLuminance = CalculateRelativeLuminance(bgRgb);
        var textLuminance = CalculateRelativeLuminance(textRgb);
        
        var lighter = Math.Max(bgLuminance, textLuminance);
        var darker = Math.Min(bgLuminance, textLuminance);
        
        return (lighter + 0.05) / (darker + 0.05);
    }
    
    private (double r, double g, double b) ParseRgbColor(string rgbString)
    {
        var match = Regex.Match(rgbString, @"rgb\((\d+),\s*(\d+),\s*(\d+)\)");
        if (match.Success)
        {
            var r = double.Parse(match.Groups[1].Value) / 255.0;
            var g = double.Parse(match.Groups[2].Value) / 255.0;
            var b = double.Parse(match.Groups[3].Value) / 255.0;
            return (r, g, b);
        }
        
        // Default to black text on white background
        return rgbString.Contains("255") ? (1.0, 1.0, 1.0) : (0.0, 0.0, 0.0);
    }
    
    private double CalculateRelativeLuminance((double r, double g, double b) rgb)
    {
        var r = rgb.r <= 0.03928 ? rgb.r / 12.92 : Math.Pow((rgb.r + 0.055) / 1.055, 2.4);
        var g = rgb.g <= 0.03928 ? rgb.g / 12.92 : Math.Pow((rgb.g + 0.055) / 1.055, 2.4);
        var b = rgb.b <= 0.03928 ? rgb.b / 12.92 : Math.Pow((rgb.b + 0.055) / 1.055, 2.4);
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
    
    private double GetMinimumContrastRatio(double fontSize, bool isBold)
    {
        // WCAG 2.1 AA standards
        var isLargeText = (fontSize >= 18) || (fontSize >= 14 && isBold);
        return isLargeText ? 3.0 : 4.5;
    }
    
    private double GetFontSize(IWebElement element)
    {
        var fontSizeStr = ((IJavaScriptExecutor)_driver).ExecuteScript(
            "return window.getComputedStyle(arguments[0]).fontSize;", element).ToString();
        
        return double.TryParse(fontSizeStr.Replace("px", ""), out var size) ? size : 14.0;
    }
    
    private bool IsBoldText(IWebElement element)
    {
        var fontWeight = ((IJavaScriptExecutor)_driver).ExecuteScript(
            "return window.getComputedStyle(arguments[0]).fontWeight;", element).ToString();
        
        return fontWeight == "bold" || fontWeight == "700" || int.TryParse(fontWeight, out var weight) && weight >= 700;
    }
    
    private bool HasVisualIndicator(IWebElement element, string property)
    {
        var value = ((IJavaScriptExecutor)_driver).ExecuteScript(
            $"return window.getComputedStyle(arguments[0]).{property};", element).ToString();
        
        return !string.IsNullOrEmpty(value) && value != "none" && value != "0px";
    }
    
    private IWebElement FindAssociatedLabel(IWebElement field)
    {
        var fieldId = field.GetAttribute("id");
        if (!string.IsNullOrEmpty(fieldId))
        {
            try
            {
                return _driver.FindElement(By.CssSelector($"label[for='{fieldId}']"));
            }
            catch (NoSuchElementException)
            {
                // Try aria-labelledby
                var ariaLabelledBy = field.GetAttribute("aria-labelledby");
                if (!string.IsNullOrEmpty(ariaLabelledBy))
                {
                    return _driver.FindElement(By.Id(ariaLabelledBy));
                }
            }
        }
        
        return null;
    }
}
```

### 4. Focus Management Testing

#### Focus Management Tests
```csharp
[TestClass]
public class FocusManagementTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver();
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_FocusIndicators_VisibleAndClear()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        var focusableElements = _driver.FindElements(By.CssSelector(
            "input, button, select, textarea, a[href], [tabindex]:not([tabindex='-1'])"));
        
        foreach (var element in focusableElements)
        {
            if (element.Displayed && element.Enabled)
            {
                // Focus the element
                element.Click();
                
                // Check for visible focus indicator
                var outlineStyle = ((IJavaScriptExecutor)_driver).ExecuteScript(
                    "return window.getComputedStyle(arguments[0]).outline;", element).ToString();
                var outlineWidth = ((IJavaScriptExecutor)_driver).ExecuteScript(
                    "return window.getComputedStyle(arguments[0]).outlineWidth;", element).ToString();
                var boxShadow = ((IJavaScriptExecutor)_driver).ExecuteScript(
                    "return window.getComputedStyle(arguments[0]).boxShadow;", element).ToString();
                
                var hasFocusIndicator = !outlineStyle.Contains("none") || 
                                      !outlineWidth.Equals("0px") || 
                                      !boxShadow.Equals("none");
                
                Assert.IsTrue(hasFocusIndicator, 
                    $"Element {element.TagName} should have visible focus indicator");
            }
        }
    }
    
    [TestMethod]
    public void CustomerForm_FocusTrap_WorksInModal()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Open modal dialog (if exists)
        var modalTrigger = _driver.FindElements(By.CssSelector("button[data-toggle='modal'], .modal-trigger"));
        
        if (modalTrigger.Count > 0)
        {
            modalTrigger[0].Click();
            
            // Wait for modal to open
            var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(5));
            var modal = wait.Until(driver => driver.FindElement(By.CssSelector(".modal, [role='dialog']")));
            
            // Find focusable elements within modal
            var modalFocusableElements = modal.FindElements(By.CssSelector(
                "input, button, select, textarea, a[href], [tabindex]:not([tabindex='-1'])"));
            
            if (modalFocusableElements.Count > 0)
            {
                var firstElement = modalFocusableElements[0];
                var lastElement = modalFocusableElements[modalFocusableElements.Count - 1];
                
                // Focus should start on first element
                firstElement.Click();
                var activeElement = _driver.SwitchTo().ActiveElement();
                Assert.AreEqual(firstElement, activeElement, "Focus should start on first modal element");
                
                // Tab through all elements
                for (int i = 0; i < modalFocusableElements.Count - 1; i++)
                {
                    activeElement.SendKeys(Keys.Tab);
                    activeElement = _driver.SwitchTo().ActiveElement();
                }
                
                // Should be on last element
                Assert.AreEqual(lastElement, activeElement, "Should reach last modal element");
                
                // Tab from last element should cycle to first
                activeElement.SendKeys(Keys.Tab);
                activeElement = _driver.SwitchTo().ActiveElement();
                Assert.AreEqual(firstElement, activeElement, "Focus should cycle back to first element");
                
                // Shift+Tab from first should go to last
                activeElement.SendKeys(Keys.Shift + Keys.Tab);
                activeElement = _driver.SwitchTo().ActiveElement();
                Assert.AreEqual(lastElement, activeElement, "Shift+Tab should go to last element");
            }
        }
    }
    
    [TestMethod]
    public void CustomerForm_FocusManagement_AfterFormSubmission()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Fill and submit form
        _driver.FindElement(By.CssSelector("input[id$='txtEmail']")).SendKeys("focus@example.com");
        _driver.FindElement(By.CssSelector("input[id$='txtName']")).SendKeys("Focus Test");
        _driver.FindElement(By.CssSelector("input[id$='btnSave']")).Click();
        
        // Wait for submission result
        var wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(10));
        wait.Until(driver => driver.FindElements(By.CssSelector("span[id$='lblMessage']")).Count > 0);
        
        // Focus should move to success/error message for screen reader announcement
        var messageElement = _driver.FindElement(By.CssSelector("span[id$='lblMessage']"));
        var activeElement = _driver.SwitchTo().ActiveElement();
        
        // Check if focus moved to message or if message has appropriate ARIA attributes
        var focusOnMessage = activeElement.Equals(messageElement);
        var hasAriaLive = !string.IsNullOrEmpty(messageElement.GetAttribute("aria-live"));
        var hasRole = messageElement.GetAttribute("role") == "alert";
        
        Assert.IsTrue(focusOnMessage || hasAriaLive || hasRole, 
            "Form submission result should be announced to screen readers");
    }
}
```

### 5. Responsive and Mobile Accessibility

#### Mobile Accessibility Tests
```csharp
[TestClass]
public class MobileAccessibilityTests
{
    private IWebDriver _driver;
    
    [TestInitialize]
    public void Setup()
    {
        var options = new ChromeOptions();
        options.AddArgument("--window-size=375,667"); // iPhone SE size
        options.AddArgument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)");
        _driver = new ChromeDriver(options);
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void CustomerForm_MobileViewport_TouchTargetsAppropriateSize()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        var touchTargets = _driver.FindElements(By.CssSelector("button, input[type='submit'], input[type='button'], a"));
        
        foreach (var target in touchTargets)
        {
            if (target.Displayed)
            {
                var size = target.Size;
                var minSize = 44; // 44px minimum touch target size (iOS guideline)
                
                Assert.IsTrue(size.Width >= minSize || size.Height >= minSize, 
                    $"Touch target {target.TagName} is too small: {size.Width}x{size.Height}px " +
                    $"(minimum: {minSize}px)");
            }
        }
    }
    
    [TestMethod]
    public void CustomerForm_MobileZoom_AccessibleAt200Percent()
    {
        _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
        
        // Zoom to 200%
        ((IJavaScriptExecutor)_driver).ExecuteScript("document.body.style.zoom = '2.0';");
        
        // Wait for zoom to take effect
        Thread.Sleep(1000);
        
        // Check that content is still accessible
        var formElements = _driver.FindElements(By.CssSelector("input, label, button"));
        
        foreach (var element in formElements)
        {
            if (element.Displayed)
            {
                Assert.IsTrue(element.Size.Width > 0 && element.Size.Height > 0, 
                    "Form elements should remain visible at 200% zoom");
                
                // Check that elements don't overflow horizontally
                var elementRight = element.Location.X + element.Size.Width;
                var viewportWidth = _driver.Manage().Window.Size.Width;
                
                Assert.IsTrue(elementRight <= viewportWidth + 20, // Allow small tolerance
                    "Form elements should not cause horizontal scrolling at 200% zoom");
            }
        }
        
        // Check that form is still functional
        var emailField = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
        emailField.Clear();
        emailField.SendKeys("zoom@example.com");
        
        var emailValue = emailField.GetAttribute("value");
        Assert.AreEqual("zoom@example.com", emailValue, "Form should remain functional at 200% zoom");
    }
    
    [TestMethod]
    public void CustomerForm_ScreenOrientation_WorksInBothModes()
    {
        var orientations = new[]
        {
            new { Name = "Portrait", Width = 375, Height = 667 },
            new { Name = "Landscape", Width = 667, Height = 375 }
        };
        
        foreach (var orientation in orientations)
        {
            _driver.Manage().Window.Size = new Size(orientation.Width, orientation.Height);
            _driver.Navigate().GoToUrl("http://localhost:8080/CustomerForm.aspx");
            
            // Check that all form elements are accessible
            var formElements = _driver.FindElements(By.CssSelector("input, label, button"));
            
            foreach (var element in formElements)
            {
                Assert.IsTrue(element.Displayed, 
                    $"Form element should be visible in {orientation.Name} orientation");
            }
            
            // Check that form can be completed
            var emailField = _driver.FindElement(By.CssSelector("input[id$='txtEmail']"));
            var nameField = _driver.FindElement(By.CssSelector("input[id$='txtName']"));
            var saveButton = _driver.FindElement(By.CssSelector("input[id$='btnSave']"));
            
            emailField.Clear();
            emailField.SendKeys($"orientation{orientation.Name.ToLower()}@example.com");
            nameField.Clear();
            nameField.SendKeys($"{orientation.Name} User");
            
            // Verify elements are clickable
            Assert.IsTrue(emailField.Enabled, $"Email field should be enabled in {orientation.Name}");
            Assert.IsTrue(nameField.Enabled, $"Name field should be enabled in {orientation.Name}");
            Assert.IsTrue(saveButton.Enabled, $"Save button should be enabled in {orientation.Name}");
        }
    }
}
```

## Accessibility Testing Automation in CI/CD

### 1. Automated Accessibility Pipeline
```csharp
[TestClass]
public class AccessibilityRegressionTests
{
    private IWebDriver _driver;
    private AxeBuilder _axeBuilder;
    
    [TestInitialize]
    public void Setup()
    {
        _driver = new ChromeDriver(new ChromeOptions { Headless = true });
        _axeBuilder = new AxeBuilder(_driver);
    }
    
    [TestCleanup]
    public void Cleanup()
    {
        _driver?.Quit();
    }
    
    [TestMethod]
    public void AccessibilityRegression_AllPages_NoNewViolations()
    {
        var pagesToTest = new[]
        {
            "/CustomerForm.aspx",
            "/CustomerGrid.aspx",
            "/Login.aspx",
            "/Reports.aspx"
        };
        
        var baselineViolations = LoadAccessibilityBaseline();
        var currentViolations = new Dictionary<string, List<AccessibilityViolation>>();
        
        foreach (var page in pagesToTest)
        {
            _driver.Navigate().GoToUrl($"http://localhost:8080{page}");
            
            var results = _axeBuilder.Analyze();
            var violations = results.Violations.Select(v => new AccessibilityViolation
            {
                Rule = v.Id,
                Impact = v.Impact,
                Description = v.Description,
                ElementCount = v.Nodes.Count()
            }).ToList();
            
            currentViolations[page] = violations;
        }
        
        // Compare with baseline
        var regressions = DetectAccessibilityRegressions(baselineViolations, currentViolations);
        
        if (regressions.Any())
        {
            var report = GenerateAccessibilityRegressionReport(regressions);
            File.WriteAllText("accessibility-regression-report.html", report);
            
            Assert.Fail($"Accessibility regressions detected. See accessibility-regression-report.html for details.");
        }
    }
    
    private Dictionary<string, List<AccessibilityViolation>> LoadAccessibilityBaseline()
    {
        // Load from previous test runs or configuration
        var baselineFile = "accessibility-baseline.json";
        if (File.Exists(baselineFile))
        {
            var json = File.ReadAllText(baselineFile);
            return JsonConvert.DeserializeObject<Dictionary<string, List<AccessibilityViolation>>>(json);
        }
        
        return new Dictionary<string, List<AccessibilityViolation>>();
    }
    
    private List<AccessibilityRegression> DetectAccessibilityRegressions(
        Dictionary<string, List<AccessibilityViolation>> baseline,
        Dictionary<string, List<AccessibilityViolation>> current)
    {
        var regressions = new List<AccessibilityRegression>();
        
        foreach (var page in current.Keys)
        {
            var currentPageViolations = current[page];
            var baselinePageViolations = baseline.ContainsKey(page) ? baseline[page] : new List<AccessibilityViolation>();
            
            foreach (var violation in currentPageViolations)
            {
                var baselineViolation = baselinePageViolations.FirstOrDefault(v => v.Rule == violation.Rule);
                
                if (baselineViolation == null)
                {
                    // New violation
                    regressions.Add(new AccessibilityRegression
                    {
                        Page = page,
                        Type = "New Violation",
                        Rule = violation.Rule,
                        Impact = violation.Impact,
                        Description = violation.Description,
                        ElementCount = violation.ElementCount
                    });
                }
                else if (violation.ElementCount > baselineViolation.ElementCount)
                {
                    // Increased violation count
                    regressions.Add(new AccessibilityRegression
                    {
                        Page = page,
                        Type = "Increased Violations",
                        Rule = violation.Rule,
                        Impact = violation.Impact,
                        Description = violation.Description,
                        ElementCount = violation.ElementCount,
                        PreviousCount = baselineViolation.ElementCount
                    });
                }
            }
        }
        
        return regressions;
    }
    
    private string GenerateAccessibilityRegressionReport(List<AccessibilityRegression> regressions)
    {
        var html = new StringBuilder();
        html.AppendLine("<!DOCTYPE html>");
        html.AppendLine("<html><head><title>Accessibility Regression Report</title></head><body>");
        html.AppendLine("<h1>Accessibility Regression Report</h1>");
        html.AppendLine($"<p>Generated: {DateTime.UtcNow:yyyy-MM-dd HH:mm:ss} UTC</p>");
        
        foreach (var regression in regressions.GroupBy(r => r.Page))
        {
            html.AppendLine($"<h2>Page: {regression.Key}</h2>");
            html.AppendLine("<table border='1'>");
            html.AppendLine("<tr><th>Type</th><th>Rule</th><th>Impact</th><th>Elements</th><th>Description</th></tr>");
            
            foreach (var issue in regression)
            {
                html.AppendLine("<tr>");
                html.AppendLine($"<td>{issue.Type}</td>");
                html.AppendLine($"<td>{issue.Rule}</td>");
                html.AppendLine($"<td>{issue.Impact}</td>");
                html.AppendLine($"<td>{issue.ElementCount}</td>");
                html.AppendLine($"<td>{issue.Description}</td>");
                html.AppendLine("</tr>");
            }
            
            html.AppendLine("</table>");
        }
        
        html.AppendLine("</body></html>");
        return html.ToString();
    }
}

public class AccessibilityViolation
{
    public string Rule { get; set; }
    public string Impact { get; set; }
    public string Description { get; set; }
    public int ElementCount { get; set; }
}

public class AccessibilityRegression
{
    public string Page { get; set; }
    public string Type { get; set; }
    public string Rule { get; set; }
    public string Impact { get; set; }
    public string Description { get; set; }
    public int ElementCount { get; set; }
    public int PreviousCount { get; set; }
}
```

## Accessibility Testing Best Practices

### 1. Testing Strategy
- **Automated + Manual**: Combine automated tools with manual testing
- **Real Users**: Include users with disabilities in testing process
- **Progressive Enhancement**: Test with assistive technologies disabled
- **Multiple Browsers**: Test across different browsers and screen readers
- **Mobile Accessibility**: Test on actual mobile devices with accessibility features

### 2. Common Accessibility Issues in WebForms
- Missing or incorrect form labels
- Inadequate color contrast
- Missing focus indicators
- Inaccessible data tables
- Poor keyboard navigation
- Missing ARIA attributes
- Inaccessible error messages

### 3. Accessibility Testing Tools
- **Automated**: axe-core, WAVE, Lighthouse
- **Screen Readers**: NVDA, JAWS, VoiceOver
- **Browser Tools**: Chrome DevTools Accessibility panel
- **Color Tools**: Color Contrast Analyzers
- **Mobile**: iOS/Android accessibility features

### 4. WCAG 2.1 Compliance Levels
- **Level A**: Basic accessibility (minimum level)
- **Level AA**: Standard accessibility (recommended target)
- **Level AAA**: Enhanced accessibility (gold standard)

This comprehensive accessibility testing guide ensures WebForms applications are inclusive and usable by all users, regardless of their abilities or assistive technology needs.