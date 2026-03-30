#-----------------------------------------------
#Part 3 : FILE I/O,APIs & EXCEPTION HANDLING
# THEME : PRODUCT EXPORER & ERROR - RESILIENT LOGGER
#------------------------------------------------------------
import requests
from datetime import datetime

#Shared Logger - We will create shared logger that can be used all tasks.
#Here we will approach by appending to the file each time means logs stack up across runs.

def log_error(location,error_type,message):
   # Now we will a timestamped error entry to error_log.txt
   timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   entry = f"[{timestamp}] ERROR in {location}: {error_type} - {message}\n"
   with open ("error_log.txt","a",encoding="utf-8") as f:
       f.write(entry)
    # I will also print it so that I can see errors and are visible during execution
   print(f" [logged] {entry.strip()}")   

#-----------------------------------------
#TASK 1 FILE READ & WRITE BASICS
#-----------------------------------------

print("\n" + "=" * 50)
print("    TASK 1: FILE READ & WRITE")
print("=" * 50)

#PART A : WRITE
notes = [
    "Topic 1 : Variables store data.Python is dynamically typed.",
    "Topic 2 : Lists are ordered and mutable.",
    "Topic 3 : Dictionaries store key-value pairs.",
    "Topic 4 : Loops automate repetitive tasks.",
    "Topic 5 : Exception handling prevents crashes.",
]
# Now we will write the five above required lines using 'w'mode creates or overwrites
with open("python_notes.txt","w", encoding = "utf-8") as f:
    for line in notes:
        f.write(line + "\n")
print("\n File written successfully.")  

# Now I will be adding or appending two extra lines of my own
my_extras = [
     "Topic 6 : Functions help break code into reusable chunks.",
     "Topic 7 : Modules let you import and reuse code across files.",
 ]   

with open("python_notes.txt", "a",encoding = "utf-8") as f:
    for line in my_extras:
        f.write(line + "\n")  

print("  Lines added or appended.")   

#Part B : READ  
print("\n [Reading file back : Numbered lines]")
 
all_lines = []
with open ("python_notes.txt", "r", encoding="utf-8") as f:
    # I will approach by strip each line and no trailing \n in the output
    for i, line in enumerate (f,start = 1):
        clean = line.rstrip("\n")
        all_lines.append(clean)
        print(f" {i} . {clean}") 
print(f"\n Total lines in file : {len(all_lines)}")


# Keyword search wich is case insensitive
keyword = input(f"\n Enter a keyword to search for: ").strip()
matches =[line for line in all_lines if keyword.lower() in line.lower()]    

if matches:
    print(f"\n Lines containing '{keyword}' :")  
    for line in matches:
        print(f"  -> {line}") 
else:
    print(f" No lines found containing '{keyword}' . ")   

#----------------------------------------------
#TASK 2 : API INTEGRATION
#--------------------------------------------------
print("\n\n" + "=" * 50)  
print("  TASK 2 : API INTEGRATION")
print("="* 50)  

BASE_URL = "https://dummyjson.com/products"     

# STEP 1 : FETCHING AND DISPLAYING 20 PRODUCTS:
print("\n [Fetching 20 products from DummyJSON....]\n")
products = []   # I will be using this list  again for step 2

try:
    resp = requests.get(f"{BASE_URL}?limit=20",timeout=5)
    
    #We will check status manually as HTTP errors(404 etc) don't raise exceptions
    if resp.status_code == 200 :
        data = resp.json()
        products = data["products"]
        
        #Header of the Table
        print(f"{'ID':<4}| {'Title': <30} | {'Category':<14}| {'Price':>8}| {'Rating':>6}")
        print(" " + "-" * 70)
        
        for p in products:
            print(f"{p['id']:<4}| {p['title'][:30]:<30} | "
                  f"{p['category'][:14]:<14}| ${p['price']:>7.2f} | {p['rating']:>6}")
    
    else:
        msg =f"HTTP {resp.status_code} from products endpoint"
        print(f"  x{msg}")
        log_error("fetch_products", "HTTPError", msg)

except requests.exceptions.ConnectionError:
    msg = "No connection could be established"
    print(" Connection failed. Please check you Internet connection.")
    log_error("fetch_products", "ConnectionError",msg)
           
except requests.exceptions.Timeout:
    print("  Repeat timed out. Try again later.")
    log_error("fetch_products","Timeout", "Request exceeded 5 seconds") 

except Exception as e:
    print(f" Unexpected error: {e}")
    log_error("fetch_products", "Exception", str(e))   


#STEP 2 : Filter rating >=4.5 and we will be sirting it by price in descending order
print("\n [Products with rating >= 4.5,sorted by price ,high to low ]\n") 

if products :
    # I will approach this by filtering first and then sorting
    top_picks = [p for p in products if p["rating"]>= 4.5]
    top_picks.sort(key = lambda p:p["price"], reverse = True)
    
    print(f" {'Title' : <32} | {'Price':>8} | {'Rating':>6}")
    print(" " + "-" * 55)  
    for p in top_picks:
        print(f"{p['title'][:32]:<32} | ${p['price']:>7.2f}|{p['rating']:>6}")
else:
    print("(No products fetched , so skipping filtering )")    

#STEP 3: Fetching Laptps by category
print("\n[Fetching Laptops category....]\n")

try:
    resp = requests.get(f"{BASE_URL}/category/laptops",timeout = 5)
    
    if resp.status_code ==200:
        laptops = resp.json()["products"]
        print(f"{'Laptop':<35} | {'Price':>9}")
        print(" " + "-" * 48)
        for lap in laptops:
            print(f" {lap['title'][:35]:<35} | ${lap['price']:>8.2f}")
    else : 
         msg = f"HTTP {resp.status_code} from laptops category"
         print(f" x {msg}")   
         log_error("fetch_laptops", "HTTPError",msg)


except requests .exceptions.ConnectionError:
      print(" Connection failed. Please check your internet connection.")
      log_error("fetch_laptops", "ConnectionError","No connection could be made")

except requests.exceptions.Timeout :
      print("Connection Failed. Please Check your Internet connection.") 
      log_error("fetch_laptops","Timeout", "Request exceeded 5 seconds")

except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("fetch_laptops", "Exception", str(e))     


#STEP4 POST A NEW PRODUCT 
print("\n [Sending POST request to add a product .....]\n")   

new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
    
}  

try:
   resp = requests.post(f"{BASE_URL}/add", json=new_product,timeout=5)
   
   if resp.status_code in (200,201):
        print("✓ POST response:")
        print(f"{resp.json()}")   
   else:
       msg =f"HTTP {resp.status_code}"  
       print(f" x {msg}")  
       log_error("post_product", "HTTPError", msg)

except requests.exceptions.ConnectionError:
       print(" Connection failed.")
       log_error("post_product","ConnectionError","No conection could be made")

except requests.exceptions.Timeout :
       print(" Requests timed out.")
       log_error("post_product","Timeout", "Request exceeded 5 seconds")           

except Exception as e:
      print(f" Unexpected error:{e}")
      log_error("post_product","Exception",str(e))

#--------------------------------------------------
# TASK 3 EXCEPTION HANDLING
#-------------------------------------------------------

print("\n\n" + "=" * 50)
print( " TASK 3: EXCEPTION HANDLING") 
print("=" * 50)

#PART A : Guarded Calculator 
def safe_divide(a,b):
    # Here I decided to go with returning strings for errors so that the caller always gets something
    #It is usable without crash and none
    try:
        return a/b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error : Invalid input types" 

print("\n [Part A safe_divide tests]")
print(f" safe_divide(10,2)  ->{safe_divide(10,2)}")
print(f"  safe_divide(10,0)  ->{safe_divide(10,0)}") 
print( f" safe_divide(ten,2)  ->{safe_divide('ten',2)}") 

#PART B : GUARDED FILE READER:
def read_file_safe(filename):
    # This is to open and return file contents , and handles error gracefully
    try:
        with open(filename,"r", encoding="utf-8") as f:
              content = f.read()
        return content      
    except FileNotFoundError:
         print(f" Error: File '{filename}' not found.")
         return None 
    finally: # finally always and runs and returns even if an exception is raised 
        print(f" File read operation attempt complete.")
print("\n [ Part B - read_file_safe tests]") 

print("\n -> Reading 'python notes.txt':")
content = read_file_safe("python_notes.txt") 
if content :
    print(f"(first 60 chars) {content[:60]}....")

print("\n  -> Reading 'ghost_file.txt' : ") 
read_file_safe("ghost_file.txt")  

# PART C : ROBUST API CALLS
# I have already done this in Task 2 ,every request in Task 2 is wrapped with try-except
# It also covers ConnectionError,Timeout and Generic Exception.
print("\n[PART C - Robust API calls already applied throughout Task 2.]")

#PART D : INPUT VALIDATION LOOP
print("\n [PART D Product ID Lookup Loop]")
print(" (type 'quit' to exit)\n")

while True:
    raw = input("Enter a product ID (1-100), or 'quit' to exit"). strip()
    
    if raw.lower() == "quit":
        print( "  Exititng Lookup")
        break

# Now validating it's actually an integer
    try:
       pid = int(raw)
    except ValueError:
         print( " ! That's not a valid intger. Try again. \n")            
         continue

#Now validating range:-
    if not(1<= pid <= 100):
         print(" ! ID must be between 1 and 100 . Try again. \n")
         continue
     
# now to make API calls now we will
    try :
       resp = requests.get(f"{BASE_URL}/{pid}",timeout=5)
    
       if resp.status_code == 200:
         p = resp.json()
         print(f" {p['title']} - ${p['price']:.2f}\n")
       elif resp.status_code == 404:
         print(f" Product not found.\n")
         log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {pid}")
    
       else:  
         print(f" Unexpected status:{resp.status_code}\n") 

    except requests.exceptions.ConnectionError:
     print("Connection failed .Please check yout internet connection. \n")      
     log_error("lookup_product", "ConnectionError", "No connection could be made")  

    except requests.exceptions.Timeout:
     print(" Request timed out.Try again later.\n")
     log_error("lookup_product","Timeout","Request exceeded 5 seconds")

    except Exception as e:
     print(f" Unexpected error: {e}\n")
     log_error("lookup_product", "Exception",str(e))


#----------------------------------
# TASK 4 LOGGING TO FILE
#----------------------------------------
print("\n\n" + "="*50)
print("    TASK 4: LOGGING TO FILE")
print("=" * 50)

#Intentional trigger 1: ConnectionError from unreachable URL
print("\n [Trigger 1 ConnectionError via bad URL]")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError:
      print(" Connection failed.Please check your internet connection.")  
      log_error("fetch_products", "ConnectionError", "No connection could be made")   
except requests.exceptions.Timeout:
    print(" Request timed out.")
    log_error("fetch_products","Timeout", "Unreachable host timed out")
except Exception as e:
    log_error("fetch_products","Exception", str(e))
    
#Intentional trigger 2: HTTP 404 from a non existent product
print("\n [Trigger 2 - HTTP 404 for product ID 999]")    
try:
    resp = requests.get(f"{BASE_URL}/999", timeout = 5)
    if resp.status_code != 200:
          # we will detect by checking status_code
         log_error("lookup_product","HTTPError",f"404 Not Found for product ID 999")
         print(f" ProductID 999 not found(status{resp.status_code}).")
    else:
        print(f"Unexpectedly found:{resp.json().get('title')}")
except requests.exceptions.ConnectionError:
       print(" Connectio failed.")
       log_error("lookup_product","ConnectionError","No connection could be made") 
except Exception as e:
    log_error("lookup_product","Exception",str(e))
    
# Now printing the full error log:
print("\n [Contents of error_log.txt]")
print(" " + "-" * 50)

log_content = read_file_safe("error_log.txt")
if log_content:
    for line in log_content.strip().split("\n"):
        print(f"{line}")
else:
    print(" (log file is empty or missing)") 


print("\n" + "=" * 50)
print("  ALL TASKS COMPLETE")
print("=" * 50 + "\n")

                                                           