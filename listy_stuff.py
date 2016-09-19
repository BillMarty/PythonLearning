#Playing around
#Verify my observation about squares being sum of odds
#Changed file encoding from UTF-8 to ASCII

#How many squares am I going to check?
limit = 100

squares = []
odds = [1]
for n in range(1, limit+1):
    squares.append(n**2)
    odds.append(odds[-1] + 2)

#Get rid of the extra value at the end of odds.
odds.pop()

if limit < 50:
    print('squares = ' + str(squares))
    print('odds = ' + str(odds))

sum_of_odds = []
# n is the number we are squaring, and the number of odds we are summing.
for n in range(1, limit+1):
    sum = 0
    for n_index in range(0, n):
        sum = sum + odds[n_index]
    sum_of_odds.append(sum)
    # print('n, nn, sum_of_odds: ' + str(n) + ', ' + str(n_index) + ', ' + str(sum_of_odds))

print('sum_of_odds = ' + str(sum_of_odds))

# Now, are squares and sum_of_odds the same lists?
if squares == sum_of_odds:
    print('The lists match! Your observation is verified :-)')
else:
    print('Hmmm... the lists differ.')

# -----------------------------------
# Program above complete and working.
# Now adding some lines to exercise slices.
# -----------------------------------
print('The 1st three squares are: ' + str(squares[:3]))
print('The last three squares are: ' + str(squares[-5:]))