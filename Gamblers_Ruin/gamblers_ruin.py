import numpy as np
import pandas as pd
from scipy.stats import sem, t

class GamblersRuin(object):
	'''
	A gambler starts with reserves of $i and plays a sequence of rounds until either i) he/she 
	loses and is "ruined" (loses all $i) or ii) wins and accumulates a total wealth of $N.
	At each round, the probability of the gambler winning is probability p and we assume that 
	every round is independent and identically distributed.
	p: probability that gambler is successful/ wins at each round.
	m: gambler's initial amount of money/reserves
	N: amount of money that the gambler hopes to reach in order to win the game.
	'''
	def __init__(self, p, i, N):
		self.p = p
		self.i = i
		self.N = N
		self.bal = i
		self.q = 1 - self.p

	def gamble(self):
		sim_results = {}

		while self.bal > 0 and self.bal < self.N:
			outcome = np.random.uniform(0,1)

			if outcome < self.p:
				self.bal += 1
			else:
				self.bal -= 1

			sim_results[outcome] = [self.bal]
		
		result = pd.DataFrame.from_dict(sim_results, orient='index').reset_index().rename(columns={'index':'outcome', 0:'balance'})
		
		return result	

	def n_simulations(self, games=100):
		self.df_outcome = pd.DataFrame()

		for game in np.arange(1,games+1):
			self.bal = self.i
			res = self.gamble()
			res['game'] = game
			res = res.reset_index(drop=False).rename(columns={'index':'round'})
			res['round'] = res['round'] + 1
		
			self.df_outcome = pd.concat([self.df_outcome, res[['game', 'round', 'balance']]], axis=0)
			
		return self.df_outcome
		
	def probability_win(self):
		if self.p == self.q:
			prob_win = self.i/self.N
		else:
			prob_win = (1 - ((self.q/self.p) ** self.i))/(1 - ((self.q/self.p) ** self.N))
		return prob_win

	def probability_ruin(self):
		if self.p > 0.5:
			prob_ruin = 1 - ((self.q/self.p) ** self.i)  
		else:
			prob_ruin = 1
		return prob_ruin

	def observed_perc(self):
		balance = list(self.df_outcome.loc[(self.df_outcome.balance==0) | (self.df_outcome.balance==self.N)]['balance'].copy())
		
		# Save final outcomes of each game to a list: 0 for ruin, 1 for achieving N
		final_outcome = list(map(lambda x: 0 if x==0 else 1, balance))

		conf_int = 0.95
		obs_mean, obs_std_err = np.mean(final_outcome), sem(final_outcome)
		obs_conf_int = obs_std_err * t.ppf((1 + conf_int)/2, len(final_outcome)-1)

		return obs_mean, obs_conf_int


