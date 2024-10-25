import gmpy2
import time
import random
class Paillier(object):
    def __init__(self , public_key = None, private_key = None):
        self.public_key = public_key
        self.private_key = private_key

    def __create_prime__(self , rs):
        r = gmpy2.mpz_urandomb(rs, 1024)
        while not gmpy2.is_prime(r):
            r += 1
        return r

    def __L__(self, x , N):
        tmp = gmpy2.f_div(x - 1 , N)
#        tmp = gmpy2.mpz(tmp)
        return tmp

    def __generate_key__(self):
        rs = gmpy2.random_state(int(time.time()))
        p = self.__create_prime__(rs)
        q = self.__create_prime__(rs)
        while not gmpy2.gcd(p * q, (p - 1) * (q - 1)):
            p = self.__create_prime__(rs)
            q = self.__create_prime__(rs)
        N = p * q
        lam = gmpy2.lcm(p - 1, q - 1)
        while(True):
            g = random.randint(1,pow(N,2))
            t = self.__L__(gmpy2.powmod(g,lam,pow(N,2)),N)
            if(gmpy2.gcd(t,N) == 1):
                break
        mu = gmpy2.invert(t,N)
        
        self.public_key = [N , g]
        self.private_key = [lam , mu]
        return

    def encrypt(self , plaintext):
        text = int(plaintext)
        N , g = self.public_key
        r = random.randint(0,N-1)
        cipher = gmpy2.powmod(g , text , N**2) * gmpy2.powmod(g , N , N**2)
        return cipher
    
    def decrypt(self , cipher):
        lam , mu = self.private_key
        N , g = self.public_key
        tmp = gmpy2.powmod(cipher , lam , N**2)
        text = (self.__L__(tmp , N) * mu) % N
        return text

if __name__ == "__main__":
    Pai = Paillier()
    Pai.__generate_key__()
    print"Please input the first plaintext:",
    cipher1 = Pai.encrypt(input())
    print"Please input the second plaintext:"
    cipher2 = Pai.encrypt(input())
    print"Encrypting the first plaintext gets the cipher: ",
    print(cipher1)
    print"Encrypting the second plaintext gets the cipher: ",
    print(cipher2)
    print"Multiply two ciphers we get: ",
    cipher3 = cipher1 * cipher2
    print(cipher3)
    print"The plaintext decrypted by the multipation of the cipher is: ",
    plaintext3 = Pai.decrypt(cipher3)
    print(plaintext3)