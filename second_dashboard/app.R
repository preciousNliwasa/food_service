library(shiny)
library(shinydashboard)
library(plotly)
library(ggplot2)
library(leaflet)
library(jsonlite)
library(dplyr)
library(wordcloud)
library(tm)
library(SnowballC)
library(stringr)

url_ = 'https://x8hokg.deta.dev/get_food/'
df_ <- fromJSON(url_)
df_ <- as.data.frame(df_[3])
colnames(df_) <- c('Description','Food','Price','Key')

df_

url_2 = 'https://x8hokg.deta.dev/account_balances/'
df_2 <- fromJSON(url_2)
df_2 <- as.data.frame(df_2[3])
colnames(df_2) <- c('Amount','Full_Name','Time','Key')

df_2 <- select(df_2,'Full_Name','Amount','Time')

df_2

ui <- dashboardPage(skin = 'green',title = 'dashboard',
  dashboardHeader(title = tags$p(icon('spoon'),'Dashboard')),
  dashboardSidebar(
    sidebarMenu(
      menuItem(text = 'Account',tabName = 'account',icon = icon('user')),
      menuItem(text = 'Operation',tabName = 'operation',icon = icon('phone')),
      menuItem(text = 'Food',tabName = 'food',icon = icon('spoon'))
    )
  ),
  dashboardBody(
    
    tabItems(
      tabItem(tabName = 'account',
              tabsetPanel(
                tabPanel(title = 'Account Dashboard',icon = icon('dashboard'),
                         tags$br(),
                         fluidRow(
                           column(width = 6,
                                  box(height = 350,width = 300,solidHeader = T,status = 'success',
                                      fluidRow(
                                        column(12,plotlyOutput('carrier_graph',height = '320px'))
                                      ))),
                           column(width = 6,
                                  box(height = 350,width = 300,solidHeader = T,status = 'success',
                                      fluidRow(
                                        column(12,leafletOutput('loc_map',height = '320px'))
                                      )))
                         ),
                         fluidRow(
                           column(width = 8,
                                  box(height = 300,width = 400,solidHeader = T,status = 'success',
                                      fluidRow(
                                        column(12,plotlyOutput('balances_bar',height = 280))
                                      ))),
                           column(width = 4,
                                  box(height = 300,width = 300,solidHeader = T,status = 'success',
                                      tags$br(),
                                      tags$br(),
                                      fluidRow(
                                        column(12,
                                               selectInput('customers_options','Customers',choices = unique(df_2$Full_Name)))
                                      )))
                         )),
                tabPanel(title = 'Customers Dataset',icon = icon('users'),
                         tags$br(),
                         fluidRow(
                           column(12,
                                  DT::dataTableOutput('customers_dataset'))
                         )
                         ),
                tabPanel(title = 'Balance Dataset',icon = icon('money'),
                         tags$br(),
                         fluidRow(
                           column(12,
                                  DT::dataTableOutput('balance_dataset'))
                         ))
              )),
      tabItem(tabName = 'operation',
              tabsetPanel(
                tabPanel(title = 'Operations Dashboard',icon = icon('dashboard'),
                         tags$br(),
                         fluidRow(
                           column(6,
                                  box(height = 350,width = 400,status = 'success',solidHeader = T,
                                      fluidRow(
                                        column(12,
                                               plotlyOutput('orders_date',height = 330))
                                      ))),
                           column(6,
                                  box(height = 350,width = 400,status = 'success',solidHeader = T,
                                      plotOutput('word_cloud',height = 330)))
                         ),
                         fluidRow(
                           column(6,
                                  box(height = 300,width = 400,status = 'success',solidHeader = T,
                                      fluidRow(
                                        column(12,
                                               plotlyOutput('orders_bar',height = 280))
                                      ))),
                           column(6,
                                  box(height = 300,width = 400,status = 'success',solidHeader = T,
                                      fluidRow(
                                        column(12,
                                               plotlyOutput('operations_bar',height = 280))
                                      )))
                         )),
                tabPanel(title = 'Operations Dataset',icon = icon('pen'),
                         tags$br(),
                         fluidRow(
                           column(12,DT::dataTableOutput('operations_dataset'))
                         )),
                tabPanel(title = 'Orders Dataset',icon = icon('phone'),
                         tags$br(),
                         fluidRow(
                           column(12,DT::dataTableOutput('orders_dataset'))
                         ))
              )),
      tabItem(tabName = 'food',
              tabsetPanel(
                tabPanel(title = 'Food Dataset',icon = icon('spoon'),
                         tags$br(),
                         fluidRow(
                           column(8,DT::dataTableOutput('food_dataset')),
                           column(4,box(height = 550,width = 300,solidHeader = T,status = 'success',
                                        tags$br(),
                                        selectInput('meal_options',label = 'Meal',choices = unique(df_$Food)),
                                        tags$br(),
                                        tags$br(),
                                        fluidRow(
                                          column(10,offset = 1,
                                                 box(height = 200,width = 350,solidHeader = T,status = 'success',
                                                     fluidRow(
                                                       column(12,textOutput('meal_description'))
                                                     )))
                                        )))
                         )),
                tabPanel('Menu Dataset',icon = icon('table'),
                         tags$br(),
                         fluidRow(
                           column(12,DT::dataTableOutput('menu_dataset'))
                         ))
              ))
    )
  ))

server <- shinyServer(function(input,output){
  
  
customers_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/get_customers/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  colnames(ddf22) <- c('Email','Full_Name','Location','Phone_Number','Key')
  
  df <- select(ddf22,'Full_Name','Email','Phone_Number','Location')
  
  df
  
})


balance_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/account_balances/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  colnames(ddf22) <- c('Amount','Full_Name','Time','Key')
  
  df <- select(ddf22,'Full_Name','Amount','Time')
  
  df
  
})

food_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/get_food/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  colnames(ddf22) <- c('Description','Food','Price','Key')
  
  ddf22
  
})

menu_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/get_menu/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  colnames(ddf22) <- c('Food','Time','Key')
  
  select(ddf22,Food,Time)
  
})

operations_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/get_all_operations/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  
  colnames(ddf22) <- c('Message','Operation','User','Key','Time')
  
  select(ddf22,'User','Message','Operation','Time')
  
})

corpus_ <- reactive({
  
  corpus__ <- VCorpus(VectorSource(operations_data()$Message))
  
  corpus__ <- tm_map(corpus__,removeWords,stopwords())
  corpus__ <- tm_map(corpus__,removePunctuation)
  corpus__ <- tm_map(corpus__,removeNumbers)
  
  corpus__
  
})

output$word_cloud <- renderPlot({
  
  wordcloud(corpus_(),random.color = F,colors = c('red','green','blue','black','orange','yellow'))
  
  
})


orders_data <- reactive({
  
  
  url3 = 'https://x8hokg.deta.dev/get_orders/'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3[3])
  
  colnames(ddf22) <- c('Food','User','Price','Time','Key')
  
  select(ddf22,'User','Food','Price','Time')
  
})

output$orders_bar <- renderPlotly({
  
  df <- as.data.frame(table(orders_data()$Food))
  colnames(df) <- c('Food','Counts')
  
  ggplotly(ggplot(df,aes(x = Food,y = Counts,fill = Food)) + geom_col() + labs(title = 'Orders By Food') + theme(plot.title = element_text(hjust = 0.5,face = 'bold')) + theme(panel.background = element_rect(fill = 'peachpuff')))
  
})

output$operations_bar <- renderPlotly({
  
  df <- as.data.frame(table(operations_data()$Operation))
  colnames(df) <- c('Operations','Counts')
  
  ggplotly(ggplot(df,aes(x = Operations,y = Counts,fill = Operations)) + geom_col() + labs(title = 'Operations By Type') + theme(plot.title = element_text(hjust = 0.5,face = 'bold')) + theme(axis.text.x = element_text(colour = 'white')) + theme(panel.background = element_rect(fill = 'peachpuff')))
  
})

output$customers_dataset <- DT::renderDataTable({
  
  dt = customers_data()
  dt
  
})

output$balance_dataset <- DT::renderDataTable({
  
  dt = balance_data()
  dt
  
})

output$balances_bar <- renderPlotly({
  
  dt = filter(balance_data(),Full_Name == input$customers_options)
  
  ggplotly(ggplot(dt,aes(x = Time,y = Amount)) + geom_point(color = 'blue') + labs(title = 'Balance By Time') + theme(plot.title = element_text(hjust = 0.5,face = 'bold')) + theme(axis.text.x=element_text(colour = 'white')) + theme(panel.background = element_rect(fill = 'peachpuff')))
  
  #dt <- arrange(dt,Time)
  
  #plot_ly(x = dt$Time,y = dt$Amount,type = 'scatter',mode = 'lines')
  
  
})

output$food_dataset <- DT::renderDataTable({
  
  dt <- select(food_data(),'Food','Price')
  
  dt
  
})

output$carrier_graph <- renderPlotly({
  
  url3 = 'https://0ryjmo.deta.dev/labels'
  df3 <- fromJSON(url3)
  ddf22 <- as.data.frame(df3)
  
  df <-  as.data.frame(table(ddf22))
  
  colnames(df) <- c('Carrier','Counts')
  
  ggplotly(ggplot(df,aes(x = Carrier,y = Counts,fill = Carrier)) + geom_col() + coord_flip() + labs(title = 'Accounts By Carrier') + theme(plot.title = element_text(hjust = 0.5,face = 'bold')) + theme(axis.text.x=element_text(colour = 'white')) + theme(panel.background = element_rect(fill = 'peachpuff')))
  
})

output$operations_dataset <- DT::renderDataTable({
  
  dt = operations_data()
  dt
  
})

output$orders_dataset <- DT::renderDataTable({
  
  dt = orders_data()
  dt
  
})



output$orders_date <- renderPlotly({
  
  dt <- orders_data()
  
  ggplotly(ggplot(dt,aes(x = Time,y = Price)) + geom_point(color = 'blue') + labs(title = 'Orders By Time') + theme(plot.title = element_text(hjust = 0.5,face = 'bold')) + theme(axis.text.x=element_text(colour = 'white')) + theme(panel.background = element_rect(fill = 'peachpuff')))
  
})

output$meal_description <- renderText({
  
  dt <- select(filter(food_data(),Food == input$meal_options),Description)
  paste(as.character(dt))
  
})

output$menu_dataset <- DT::renderDataTable({
  
  dt = menu_data()
  dt
  
})
  
output$loc_map <- renderLeaflet({
  

  df <- read.csv('host_coord.csv',header = T)
  
  df2 <- customers_data()
  
  loc <- as.data.frame(table(df2$Location))
  
  colnames(loc) <- c('place','count')
  
  final <- inner_join(loc,df)
  
  map000 <- leaflet(final) %>% addTiles() %>% setView(lng = 35.33405,lat = -15.39125,zoom =16) %>%
    addCircles(lng = ~lon,lat = ~lat,label = ~paste(place,':',count))
  map000
   
})
  
  
})

shinyApp(ui,server)