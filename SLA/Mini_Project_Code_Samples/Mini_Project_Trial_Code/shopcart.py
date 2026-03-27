cart = []         #holds the cart items
item_price = []   #holds the price of each item
 
while True:
    if cart:
        #call the view cart function so that the shopping cart is always on display
        pass  #remove this line when the function has been defined
    else:
        print("\nYour shopping cart is empty.\n")    
    print("Shopping Cart Options\n")
    print ("1. Add items")
    print ("2. Remove Items")
    print ("3. Quit")
  
    option = input("> ")
 
    if option == '1':
        #call the add items function
        pass #remove this line when the function has been defined
 
    if option == '2':
        if cart:
            #call the remove items function
            pass #remove this line when the function has been defined
        else:
            print("\nThere are no items in your shopping cart.\n")
 
    if option == '3':
        if cart:
            #warn the user that there are items in the shopping cart and get positive feedback before quitting
            pass #remove this line when the above in functional 
        else:
            print("\nYour shopping cart is empty.\n")
            check = "yes"
        if check == "yes":
            print("\nApplication exit")
            break