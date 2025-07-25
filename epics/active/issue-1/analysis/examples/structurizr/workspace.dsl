workspace "E-Commerce Platform" "Architecture workspace for an e-commerce system" {

    model {
        customer = person "Customer" "A customer purchasing products" {
            tags "Person"
        }

        ecommerceSystem = softwareSystem "E-Commerce System" "Allows customers to browse and purchase products online" {
            webApp = container "Web Application" "Provides e-commerce functionality to customers via their web browser" "Angular" {
                tags "Web Browser"
            }
            
            apiApp = container "API Application" "Provides e-commerce functionality via JSON/REST API" "Java, Spring Boot" {
                tags "Spring Boot"
                
                userController = component "User Controller" "Handles user registration and authentication" "Spring MVC Controller"
                productController = component "Product Controller" "Manages product catalog" "Spring MVC Controller"
                orderController = component "Order Controller" "Handles order processing" "Spring MVC Controller"
                paymentService = component "Payment Service" "Integrates with payment gateway" "Spring Service"
                notificationService = component "Notification Service" "Handles email notifications" "Spring Service"
                shippingService = component "Shipping Service" "Manages shipping integration" "Spring Service"
            }
            
            database = container "Database" "Stores user registration information, product catalog, orders, etc." "PostgreSQL" {
                tags "Database"
            }
        }

        emailSystem = softwareSystem "Email System" "SendGrid for sending transactional emails" {
            tags "External System"
        }
        
        shippingSystem = softwareSystem "Shipping System" "FedEx/UPS API for shipping management" {
            tags "External System"
        }
        
        paymentGateway = softwareSystem "Payment Gateway" "Stripe/PayPal for payment processing" {
            tags "External System"
        }

        # Relationships
        customer -> webApp "Uses" "HTTPS"
        webApp -> apiApp "Makes API calls to" "JSON/REST"
        
        # Component relationships
        webApp -> userController "Calls" "JSON/REST"
        webApp -> productController "Calls" "JSON/REST"
        webApp -> orderController "Calls" "JSON/REST"
        
        userController -> database "Reads from and writes to" "JDBC"
        productController -> database "Reads from and writes to" "JDBC"
        orderController -> database "Reads from and writes to" "JDBC"
        
        orderController -> paymentService "Uses"
        orderController -> notificationService "Uses"
        orderController -> shippingService "Uses"
        
        paymentService -> paymentGateway "Processes payments using" "REST API"
        notificationService -> emailSystem "Sends emails using" "SMTP"
        shippingService -> shippingSystem "Ships products using" "REST API"
    }

    views {
        systemContext ecommerceSystem "SystemContext" {
            include *
            autoLayout
        }

        container ecommerceSystem "Containers" {
            include *
            autoLayout
        }

        component apiApp "Components" {
            include *
            autoLayout
        }

        styles {
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "External System" {
                background #999999
                color #ffffff
            }
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape cylinder
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
            element "Web Browser" {
                shape WebBrowser
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}