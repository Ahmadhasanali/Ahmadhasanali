import sqlite3
import random
db = sqlite3.connect('database.db')
c=db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data(name TEXT , highscore REAL)")
db.commit()

def welcome(name,highscore): # Display the welcoming message 
    print("                    Hello {} ! \n\n                    Selamat datang di game Matematik \n\n                    Skor tertinggi anda adalah : {}\n\n____________________________________________________________\n\n".format(name,highscore))
    input("Tekan 'ENTER' untuk Memulai")
    
def main():
    print("____________________________________________________________\n\n                         [GAME MATEMATIK]\n\n____________________________________________________________\n")
    data=c.execute("SELECT * FROM data")

    # Count the number of the table's rows 
    x=0
    for i in data:
        x=x+1
        
    if x==0: # If empty (first run)
        # Ask about the user name
        ask=True
        while ask:
            try:
                name = input("[+] Masukkan namamu : ")
                if name=="" or len(name)==0:
                    print("Masukkan nama dengan benar!")
                else:
                    ask=False                
            except valueError:
                print("Masukkan nama dengan benar!")
                askName()
                
        print("\n___________________________________________________________\n")
        c.execute("INSERT INTO data VALUES(?,?)",(name,"0")) # Set the name in database 
        db.commit()  
        welcome(name,"0")
        highscore=0
        
    else: # User played before
        data=c.execute("SELECT * FROM data")
        for i in data: # Get the name and highscore        
            name=i[0]
            highscore=i[1]
        welcome(name,highscore)
        
    score=0
    lose=False
    while lose!=True:
        calc=random.randint(0,1) # Generate a random calculation type 0=[+] 1=[*]

        if calc==0: #(+)
            fnum=random.randint(2,50) # First number
            snum=random.randint(2,50) # Second number
            result=fnum+snum
            inp="[+] {} + {} = " # User input text
            
        else: #(*)
            fnum=random.randint(1,10)
            snum=random.randint(1,10)
            result=fnum * snum
            inp="[+] {} * {} ="
            
        def askUser(): # Ask user what is the result
                userInput=input(inp.format(fnum,snum))
                try:
                    userInput=int(userInput) # Try to make input as int
                    return userInput
                except: # If user input a text or leaft it empty
                    print("Enter a valid value")
                    askUser() # Reask again
        userInput=askUser()
        
        if userInput==result: # Correct answer 
             score=score+1 
             if score>highscore: # If this score is the high score 
                 c.execute("UPDATE data SET highscore =  ? WHERE name = ?",(score,name)) # Change highscore in database
                 db.commit()
                 print("BENAR! , anda mencapai High score! Skor Anda : {} ".format(score)) # Show message
             else: # The score is not the highscore
                 print("BENAR! Skor Anda : {}".format(score))

        else: # Wrong answer
            score=0
            print("Eh! Jawaban anda salah!")
            userAgain=input("[+] Ulangi permainan? (y,n) : ").lower()
            if userAgain=="n":
                print("Dadaah, belajar yang giat ya!")
                db.close()
                lose=True
main()

