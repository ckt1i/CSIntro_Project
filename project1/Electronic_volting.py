import gmpy2
import random 
import time 
import Paillier

if __name__ == "__main__":
    print"Please input the number of candidates."
    can_num = int(raw_input())
    print"Please input the number of elector"
    vot_num = int(raw_input())
    Pai = Paillier.Paillier()
    Pai.__generate_key__()
    vote_num = [0]*can_num
    vot_cipher = Pai.encrypt(1)
    votes_ciphered = [vot_cipher] * can_num

    for i in range(vot_num):
        print"Please type the number to vote for the candidaters:"
        vot = int(raw_input())
        while(vot < 1 or vot > can_num):
            print"Wrong input , please input again"
            vot = int(raw_input())
        votes_ciphered[vot - 1] *= vot_cipher
        print"The count of the vote have been sent with encryption"
    
    for i in range(0,can_num):
        vote_num[i] = Pai.decrypt(votes_ciphered[i])
        print"The vote count for candidate",(i + 1),"is",(vote_num[i]-1)
    
    max_vote = max(vote_num)
    max_can_num = vote_num.index(max_vote) + 1
    print"The max of the votes is No.",max_can_num,"with ",max_vote,"votes."