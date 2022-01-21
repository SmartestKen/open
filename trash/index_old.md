### season vs stationary?

### show we input slope or magnitude?	
### how many times to get familiar?
	3 times of direct conversation (time discounted though)
### how to use Kolmogorov's zero-one law
	any tail event, i.e., those events whose occurrence can still be determined if an arbitrarily large but finite initial segment of the random sequence is removed.
	
	K 0-1 law: tail event happens with either probability 0 or 1
### how to make the team productive
	you form the problem and ask them to solve it. You do not ask them to generate idea (also they are encouraged to do so).

### what is duration and convexity
	Note the current value of bond depends on the risk free rate (during pull back). Hence, YTM is influenced by risk free rate (also called interest rate)

	\deltaP/\delta y = DP
	Hence D is the first derivative of P with respect to y

	dp/p = -Ddy + (1/2)*
	f(y) = f(y_old) + f'(y_old)dy + (1/2)f''(y_old)(dy)^2
	Hence f(y) - f(y_old) = f'(y_old)dy + (1/2)f''(y_old)(dy)^2

	Do not do exponential smoothing. 
	
### should we use ES???
	do not use ES
### what statistics test to use?
	contingency table one 
	Ask about trace test and also an example
### what to do beyond SPY? How to implement linear classifier?
	for further doing than single SPY trend, use crosssectional.
		highest stock - lowest stock to predict trend
		momentum crashes moskowitz pederson -> multiple stocks

### how does training() work
	compute state by looking backwards
	
	feed into nn and get output value (can be policy/value). Decide action based on that. (Alternatively, try it later, policy network that softmax into probability, the target policy is defined to be the softmax of actual rewards)
	
	if current_pt is a new_high or new_low:
		then everything in the queue can claim reward (along with the current Q(s,a))
	
	Now put (s,a) computed this time into a queue.	


### how to choose statistics test?
	https://www.graphpad.com/support/faqid/1790/

	what to choose for this case? paired t-test or mcnemar test?
### task switch?
	consider ES or some time series techniques. Now under that setting, compare nn and chase the market classifier. Now check the best \alpha? does it differ between two classifier?
	??? check SAS tutorial 
		-> wait till later
	??? check Timmermann material
		1. design test choice
		2. EMH, not testable, does current test make sense at all?
		3. focus on empirical study or dive into those theory pattern?
		
		3. exploit the majortiy strategy used by opponent (they may be simply common people who use linear interpolation)

### how to accelerate market coding?
	if use nn, nn and backtesting function needs to be separated.

### how to accelerate?
	working version first, leave optimization and refinement as TODO. (!!! without working version, you do not even know if those optimization are on the right track)

### trend states?
	backchase, the cloest lowest/highest given range (hour/day/week/month/quarter/year) gives the slope, the average volume from those points (per minute)

### how to deal with keras input
	1. to add a layer, use np.array([..])
	2. use np_array.shape

### 280 how to show something has probability 0 or probability 1?
	first write the statement in terms of outcome set
	in HW5, we have 
	{w: radius of convergence of \sum_{n=1}^\infty X_n(w)z^n is constant c} = 1

### how to make testing network and strategy network have consistent input and output

	whether it is a reversion, if the amount of money by reverting position is more than that of holding position till next reversion...?
	
	if next one is a new low and we are at 1, then revert > hold. Otherwise, hold > revert. (This is with the assumption that market does not act like a straight line)


	Previous high/low require range to be well defined, hence equivalent to set a fix window, therefore not really removing any constraints for us


	input: given position and states
	output: linear interpolator predict revert when the slope contradict the position (5 min avg version)
	for NN
	if Q(s, hold) > Q(s, reverse), we say it predicts trend continuation
	if Q(s, hold) < Q(s, reverse), we say it predicts reversal.

	Now the correct value is set based on whether next is actually a high/low. Hence stats part finishes with t-test
	
	Now backtesting part, DQN update based on (say Q = 0 or 1). Hence completed with some benchmark (e.g. all buy)
	
	Similarly for live.

### quant statistics vs backtesting
	by efficient market hypothesis, it is impossible to predict whether it is mean reversion or trend.
	
	H_0: suppose we are at a new high (within 2 hours), NN prediction is no better than a random predictor in terms of whether it is about to revert or continue?
	H_1 NN prediction strictly better than random
	
	Now test the NN and obtain data. and apply two-tail t statistics
	
	If that works, implement the same NN + mean reversion + trend riding, along with transaction cost for backtesting. produce a stat table.
	
	Finally implement in live.
	
	
	
	1. Does hypothesized pattern/factor helps us make better than random prediction? We do not consider transaction cost as the first step decide the existence of better prediction, not whether it can overcome transaction cost.
	
	2. Now use such prediction, we implement a strategy that buy/sell in backtesting environment.
	
	3. If test stats ok, implement in live.
	
	### how to test against EMH? Is it equivalent to say random walk?
		https://economics.stackexchange.com/questions/20910/what-is-the-exact-relationship-between-the-efficient-market-and-random-walk-hypo
	
### how to deal with DRL in trading setting
	backtesting -> backtest_thread only
	live -> both backtest_thread AND live_thread
	while parent process always contain the nn training part. (i.e. thread is only responsible for delivering data for training/testing)

	use pop queue for those partial sa waiting for reward

### can we use NN for hypothesis testing? Do we use SPY or find data (possibly from Timmermann's paper? 
	check 181 courses material. what are some areas untouched yet?
		1. type I/II error, statistical testing.
		2. difference ebtween descriptive stats and inferential stats
			whether we are trying to infer population distrinbution
		3. likelihood ratio test/Lagrange multiplier test/wald test
		
			hypothesis test in general:
				1. null hypothesis, you propose a hypothetical value for a parameter
				2. now you use data to, say, get a MLE estimate). Now plug in this estimate and the hypothetical value above into the test statistics. Reject the null hypothesis depending on the statistic outcome (e.g. checking against some table).
			t-test
				null hypothesis: population mean = ...
				procedure: compute sample mean and sample error. plug in into the t-statistics and check against t-distribution table.
				
				https://en.wikipedia.org/wiki/Student%27s_t-test#Calculations
			score/lagrange test
				null hypo: para = \theta_0
				procedure: statistics only require \theta_0 and L'(\theta_0) (where L' is derivative of likelihood against \theta). Now check against \chi^2.
		
			likelihood ratio, 
				null hypothesis: para = \theta_0
				procedure: compute MLE estimate from data. evaluate L(\theta_{MLE}) and L(\theta_0). Now compute statistics and check against \chi^2.
				
			wald test:
				null hypothesis: para = \theta_0
				procedure: take MLE estimate from data. Now no need to evaluate L as the statistics can be directly computed from the estimate \theta_{MLE} and \theta_0. 
				Now check against \chi^2
			
			### the wikipedia says wald tests is easier, but why is that? Also, it looks like all three (LRT, Wald, and Lagranage/score) are using MLE and the stat follows \chi^2. What is the difference then?
				LRT require 
					1. eval L(\theta_0), 
					2. get \theta_{MLE} and L(\theta_{MLE})
				Wald requires \theta_0 and \theta_{MLE}
					1. get \theta_{MLE}
				Score requires
					1. eval L'(\theta_0)
				[check the graph from Fox](https://stats.idre.ucla.edu/other/mult-pkg/faq/general/faqhow-are-the-likelihood-ratio-wald-and-lagrange-multiplier-score-tests-different-andor-similar/)
			
			
		4. NP lemma and most powerful test
			power
				1-\beta
			p-value
				obtained from experiment. \alpha is the preset (max) threshold of rejection. Both of them are different from confidential interval. (But are connected through duality)
			
				https://ai-master.gitbooks.io/hypothesis-testing/content/duality-of-confidence-interval.html
			NP lemma
				given a fixed level \alpha, the most powerful test is the one that minimize \beta. Likelihood ratio test is one such MP test, but not necessarily the unique one. Furthermore, because LRT is always one such MP test regardless of the value of parameter, we call it UMP.
				
				difference between MP and UMP
					https://stats.stackexchange.com/questions/340953/in-plain-english-what-is-the-difference-between-a-most-powerful-test-and-a-unifo
		5. Bayesian and Contingency table
			contingency table: P(H|E) table
			Bayesian: attempt to know P(H|E) when we only have P(E|H) and P(H)

	### why is \alpha both significance level AND probability of type I error?
		if it is outside the confidential interval, we say the test is signficant and reject the null hypothesis. However, the likelihood of data falls into the rejection region WHILE the null hypothesis distribution is true (Type I error) is exacly the probability of the rejection region.

### how to categorize notes? e.g. a script that automatically fglush everything in 280A into one md file
### how to deal with sunlight??

### how to ensure task switch?
	Single task async is only considered switch when two things can be developed indepdendenly. If two directions have significant overlap, then add a distinct task and multiprocess instead.
### should we be greedy in terms of money?
	No, if money accompanied by lack of information, knowledge, network, then it is valueless. But conversely, if you have more info, knowledge and network than others, then it gives you an advantage over them.
	
	As an implication, it is NOT sufficient to do technical analyis to the time series itself.

### how do we do the statistical parts? is DRL needed or not?

### how to enable links in codeblock style
	[Here is the answer`](https://stackoverflow.com/questions/20092433/placing-links-inside-markdown-code-blocks)
### how to accelerate progress
	do not think too much, take the whatever the easiest version and realize it into a __working__ version.

### how does Q-learning update?
	https://en.wikipedia.org/wiki/Q-learning

	note we take optimal action value on next state for iterative update.
### current task switch
	AI coding
	### how to AI coding
		1. price = (high+low)/2
		2. +1/hold/-1 3 decisions
		3. DQN with LSTM design
		### there is no optimal policy, what can we do?
			reversal action reward and use DQN rather than policy netowrk
		4. explore trades/quotes later. focus on bars for now
	grpahical coding and github page
		to determine trend, you have to define the horizontal and vertical scale (they an be variable) , but they have to be defined. 
		
### what are acrions used by nn or any strategy?
	given current position and other states
	decide if current position is in line with the trend and should it be reversed (mean reversion)
	hold/reversal the states will include the position.
	now action is whether to reversal. 
	reward, the amount of delta from previous reversal (or beginning of day) till next reversal (or end of day). For reversal, it is from now to next reversal.
	### shouldn't the hold reward also start counting from now? Since we do not really know the previous decisions?
	i.e. the decision will not only decide your future reward, but also previous reward
	
	### what are some backtesting statistics we can use?
	https://elite.finviz.com/help/technical-analysis/backtests_report.ashx
	
	### how to approach new project/field
		keep it simple, minimal to achieve the goal rather all cutting edge components.
	

	


### relation between price derivative and human prediction
	dP/dt represent expected prediction, but prediction is then influence by dP/dt to certain extent.

	
	
### what should I implement for the project
	TODO 1. Deep reinforcmeent learning? given data, compute action and the reward based on action
	2. mean reversion strategy mixed with trend following
	3. benchmark

### how to decide if to use mean reversion (gradient mean, 30 day oving avg etc.) or riding trend
	is mean (gradient) close to 0? If so, then crossing mena means reversing trend and therefore we can bet at highest that it will reduce. Otherwise, if the mean is far above or below 0, then even if it cross mean, the trend continues. (hence mean reversion is only for relatively stagnant/smooth market, not suitable for big bull/bear)
	
	

### courses to select
### how to decide whether it is trending or mean reversion? volume?
	volume? or anything from latest trade/quote 
	agent can see other agent's actions and possibly know how powerful other agents are based on their action
	
	ensure you are one of the early observers (advantage over normal investors relying gui)
	
	1. analyze whether bar can let you distinguish trend and/or big boss action
	2. if not switch to trade data.
### 1. search cannot jump to target 
		imagine I search and I get a list of previous questions that I wrote. I click one of them and I directly jumped to there. 
	i.e. hierarchical searchable symbol list
	
### what is mean reversion exatly doing
	when it is very above the mean, short. when it is very below the mean, long. But this ASSUME the mean is around 0. Otherwise the arg ment does not make sense.

	when mean (return) is significantly above 0, the trend is up and vice versa
	if band up and price > band
		trend
	if band down and price < trend
		trend


	horizontal indicator: if something at t bigger than something at t-1
	vertical indicator: bollinger band, if at t bigger than at t, then possible trend, else not

### what are the distribution for shorting?
!!! language and anything that help you approach the information (physical) center is extremely beneficial


### difference between gradient (related to moving avg as well) and return
	to compute capital changes, use return. (time discount equality is also expressed in terms of return rather than gradient)
	### where to use gradient then?
		++ + top ranking in return rate
		-- - bottom ranking in return rate
		+ ++ or - -- avg ranking in return rate
		
		gradient can be used for self comparison. for cross comparison, we have to use return rate (and normalized by cap)
		
		imagine cap increase by same amount, return rate will become smaller as base (denominator cap) is now larger. But gradient (denominator is \delta t) is not influenced by that, but gradient across multiple tickers do not make sense.

		return cannot compare horizontally (along time)
		gradient cannot compare vertically (across company)
		
		hence mean reversion can either means self comparing to mean gradient across time, or comparing to mean return across companies (at a fixed time)
		### what to avoid in both theory thoughts and algorithms?
			avoid bad comparison as indicated above, avoid THRESHOLD in the program, avoid second derivative
			
			try to read into a dictionary rather than two arrays. It is always more convenient to go back from dict to list


### continue to look at related item of pair trade, use GNN to somehow achieve better performance. BUt imagine everyone is using GNN to do the same thing, your model quicly loses its profitability.


### how to make clean questions?
	i.e. not everything crunched together?
	
### is mean reversion deadling with moving averages or avg return rate?
the amount of price increase averages out. But note this do not necessarily mean it has to decrease after a sharp increase (i.e. the total area does not have to be 0), it just mean that return rate sometimes goes higher than average and sometimes lower (but need not to be negative).


### what is the approach for grabbing info?
	i.e. spend etf time on more valuable information. 
	
	if you want something out of nothing, or something huge out of somthing small, it is impossible. Hence rather than staying here trying to analyze front and abck of capitalization, find a powerful institution and join and directly learn from them. They already invested their time into all these, hence learning from them will given you much higher information gradient.
	
	i.e. you can make your information gradient high by taking *parts* of other people's result/experience. 
	You can also make it higher by reducing the amount of duplicate info (e.g. you already know it, but writing down again produce no new info while taking lots of time)

	any information has inherent value (context dependent e.g. monetary value), but the amount of time is the key. We want the highest time gradient
	
	the amount of time should be proportional to the proability that it assist you to obtain a highest gradient among all situation
	
	
	information has inherent value. at any time point, use the existing information to find the information gradient (i.e. time distribution of new info to gen/explore such that maximize our information total value at next time point)


	given a tradable pattern, then everyone discovers it and utlize it. NOw equivalent to have no pattern. Hence the question now comes to, what if we do not have pattern, how to trade?

### why not individual stocks
	for that you need to more information than the time series itself.because individual stocks are highly susceptible to their projects and events while SPY 500 is unlikely to be influenced by, say, a company's PE ratio lower than normal



	spy serve as a baseline for individual stock trend through mean reversion, but then to predict spy price we need individual stock trend.

### what is 404 lecture 5 talking about?
	https://rady-ucsd.12twenty.com/Login
	r_t = p_t - p+{t-1}
	r_t = constant + \phi r_{t-1} + noise (note that if not forecastable, then \phi coeff is 0)


	now asusme predictable
		r_t <-> p_t, coeff \beta
		p_t self AR, coeff \phi
	
	we have bias in \phi when finite samples, this results in Kendall bias
	
	Now it propagates to \beta
	 this is called Stamburgh. (NOte the negative sign)

### what is the benefit of ETF?
	growth of every dollar reflected equally in etf regardless the company in which it happens

### caution about yfinance??
	can only download one ticker at a time, extremely slow

	do not do if wiggle. But by the time we know it is wiggling, we already lose our money in it.
	
	more cross sectional info or 
	
	Hence, we must be able to somehow rpedict wiggle from external information.
### adb silence
### palse function python
### why probbility theory fail
	well , given any strategy, there exists infinitely many way such that that strategy cannot beat the etf. Those probability cannot be quantified using [0,1] interval (e.g. there is no 60% of \infty)
### what pattern is trustworthy
	steady increase
	sudden drop

	but given any threshold, is it a noise or is it a signal?
	
	use adaboost or analyze the crossover of the strategic vs etf? what situation do the algorithm miss (when/what price)
### how to make python run faster
	avoid dataframe unless reading/writing data.
### what are asusmptions when coding market
	minimize the call to databse, load once and operate in memory
	i.e. list < df < db call

	separate strategy and live/backtesting thread.

	### how to handle order on alpac
	if sign reversal, need to delete position first and switch. Do not directly jump as that will trigger 403 forbidden on alpaca
	
	if same sign, target magnitude greater, then place order(target - original)
	if same sign, target magnitude smaller, then delete position(original - target)
	if different sign, then delete position(existing), then place order(target)
	
### why cannot beat the amrket
	well, on average, the mean of next step growth is the long term averaeg, which is positive. Hence any non-always-buying strategy will fail on its shorting part after long time. Margin can do something, but it comes with interest
	
	### try one ??
		if there exists confidentally shortable pattern of time series, then it is doable. Otherwise always-buy is the only way to go.
		
		### one doubt is that we cannot use time series to beat time series. i.e. we cannot see any shortable patterns unless we choose to receive external information help (those informaiton that will fundamentally challenge people's productivity)
		
		basicall, list any of these pattern as if condition for shorting. Else buy 100%.
		
		if backtesting show it fails, then we reject the hypothesis that this is a shortable pattern.
### how to accelerate market coding
	search 403 in the following:
		https://alpaca.markets/docs/api-documentation/api-v2/
	always do 
	if 200:
		do normal stuff
	else:
		print response out (those are the error messages)
### how to teach nn hold it for higher gain
	
### how to etf distribute
	spend more time on HIGHER likelihood of MORE successful/powerful people more than ONCE. (i.e. people above you or people who have accomplished what you are trying to accomplish)
	
	
### first observer/actors does not see such thing, but the later observers can see such \beta? how do we incorporate this info into model?
	i.e. actor -> they themselves change how actors observe the phenomemon

	the action has to be incorporated into model. Otherwise model diff by actor. ENvironment as a random actor itself?

### What are restrictions on VAR?
	generalization of autoregression

### how to resolve the case that the agent wants to land in the best state for stock market?

### tools that students use
	slidespace
	electrotriton
	redshelf
	-> website -> allow html
	
### how to generate probability and range?
	softmax, or divide by range and shift.

### how is markowitz formulated
	we fixed a feasible r. then minimize the \sigma

### MDP vs MP whether there is a intermediate state


### what are the accounting statements and how to read them?
	income statement: asset_{t+1} - asset_t = revenue - expense
	cash flow statement cash_{t+1} - cash_t = total_cashflow = in_cashflow - out_cashflow
	balance sheet: asset_t = liabilities_t + equity_t
		note that liabilities are the amount of money you borrow, and these are usable funds and hence part of your asset right now.

### what is the correct formula for adjustment in position
	consider target pos as two part: current position and delta. we have
		cur_pos*cur_price + delta*state_price = total_val*target%
		
		DO NOT use target_pos*state_price directly, that does not make sense in the context of ADJUSTMENT
		
### state should not include any noisy signals, e.g. current price/amount of cash/amount of asset, otherwise neural network likely not work?
	state can include position
	moving avg diff should use subtract rather than divide as normalization. e.g. SPY +50 out of 500, QQQ +100 out of 1000, ratio is the same, but the amount of reward is different

	### s_t has to influence a_t, a_t has to influence s_{t+1}?
		### if a_t does not infleucen s_{t+1}, then it is purely a prediction problem. but what if s_t does not influence a_t?
			
	
	### how does DQN work?

### what if PPO and DQN does not work?
	https://www.google.com/search?q=michael+kearns+pennsylvania
	
### how to do math PhD while dealing with all these.
	https://www.google.com/search?q=mengdi+wang+princeton

### what would be the algorithm for get_calendar?
	prev_date = today - 1
	if calendar_http(prev_date) > today:
		today is not a trading day
	else: 
		today is and return today's stuff
		
### what are some caution about datetime when doing trading
	time difference, the rfc may always be in -4:00 UTC while datetime object may be in local time.

### how does updated version of requried_data difffer?
	version 1:
		when tradable
			get current_bar
			append to temp_bar if consecutive minute
			empty temp_bar if not consecutive_minute (or first iteration), add the cur_minute in.
		
			now try requesting everything in between [data_end +1, temp_bars[-1] - 1], write to database
	version 2:
		when tradable:
			get current_bar
			append to temp_bar if consecutive minute, POP the oldest one if gap_length reached
			empty temp_bar if not consecutive_minute (or first iteration), add the cur_minute in.
	
			now try requesting everything in between [data_end +1, temp_bars[-1] - 1], write to database
	
	the benefit of version 2 is that for history testing, we do not need to consider what is in the temp_bar. Furthermore, there will not be memory issues if running long
	
	note that we skip if we fall into neither situations for temp_bars (that is the case where one minute does not pass yet)
	

### relationship between moving average and average return
	ma_k(t) = (\int_{t-k}^t f(x)dx)/k
	ar_k(t) = (f(t) - f(t-k))/k

	assuming f has an anti-derivative F. We have
	(d/dt)ma_k(t) = (d/dt)(F(t) - F(t-k))/k = ar_k(t)
	
	Hence moving average crossover (small from below) IMPLIES
		the slope of short one higher than slope of large one iff
		ar_small(t) > ar_large(t)
	
	!!! note that the first line IMPLIES the second and third but not vice versa. (imagine two line cross over each other, ar_small(t) > ar_large(t) for all t, but cross over only happens at one particular t.)
	
	Hence moving average crossover provide more information than simple avg return comparison?
		i.e. avg return comparison is a weaken version of crossover analysis?
	
### is total area 0 along some offset (avg) return line?
	
### what would be the algorithm for prev_minute then
	if not a trading_day or now<=open:
		return previous_trading_min(previous day 23:59)
	else:
		if now > close:
			return close
		# now in the interval (open, close]
		else:
			return now - 1minute

### when to short?
	assume close to constant rate of working, (if global workers failure then that rate reduces), if keep getting higher than that rate, then short, if keep getting lower than that rate, then long
	
	slow gain -> buy <- rapid loss
	fast gain -> short <- slow loss
	
### datetime different timezone comparison (tz nive vs tz aware)
	https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end
	
	for stock market, always at entrance convert everything into NY time (or stock market time), then underlying interface always assume that time
	https://stackoverflow.com/questions/5280692/python-convert-local-time-to-another-time-zone

### moving average vs average return?
	moving avg: whether price will increase
	avg return: derivative (slope)
	
	hence comparing moving avg is equivalent to looking at (but not comparing) avg return. It does not make sense to compare the derivative.

### shorting strategy suggestions?
	https://decodingmarkets.com/strategy-shorting-shares/
	https://www.schwab.com/resource-center/insights/content/trading-up-close-short-selling-strategies
	
	moving average corssover, -> slow growth/drop
	mean reversion, extreme large growth/drop
	ETF to give overall

### what are some venture capitalist methods
	NPV, rNPV
		delta = \sum_i C_iP_i/(1+r)^i - initial_investment
		where P_i = probability of C_i appearing
	
		https://www.friday.capital/post/valuing-life-sciences-companies-using-the-rnpv-methodology
	
		note: NPV = net present value, hence our evaluation point is at present
		given a quantity k at time a, it correspond to k(1+r)^{b-a} at time b. Hence pulling back, given k at time b, it is k/(1+r)^{b-a} at time a.
		
	Venture capitalist method
		EBITDA: raw (e.g. untaxed) version of net income, usually back-computed from net income
		
		
		delta = multiplier(T)*net_income(T)/(1+r)^T - initial_investment
		ownership_estimate = initial_investment/(multiplier*net_income(T)/(1+r)^T)
		
		where
			multipler: total_stock_value/net_income of similar companies (total_stock_value is almost always the numerator, the net_income can be changed to EBITDA (in which case we call the multiplier enterprise multiple), cash_flow, sales_total or any other metrics)
			r: risk premium rate
			T: terminal time/exit time (e.g. 5 years) of VC

	Decision tree analysis (this is related to rNPV if our decision tree lies on a timeline)
		MDP. decision -> probabilistic environment -> decison... 
		Now backtrack (iteratively), for each probabilistic environment, compute the expected value and this is the value of our decision. Now take the max among all possible decisions. 
	
	https://corporatefinanceinstitute.com/resources/knowledge/valuation/valuation-methods/

	https://www.venturevaluation.com/en/methodology/valuation-methods
		note that other than DCF pull back and comparable multiple, other stuff are less commonly used (and require much more estimates)
	
	?? what is the difference between market comparables and transaction comparables
		market comparable deals with EV/EBITDA ratio. transaction comparable deals with e.g. size of M&A (merge &acquire) deal. Transaction comparable is less commonly used.
		
### pool vs mp.process

### how to terminate infinite loop subprocess
	each try/except, the except of main handle join and save. Is it possible for subprocess function not to have try,except block (i.e. it seems ctrl-c is sent to all child processes as well?
	
	https://stackoverflow.com/questions/23826695/handling-keyboard-interrupt-when-using-subproccess/23839524
	
### how to deal with shared objects?
	manager list. Note do not nest as manager proxy cannot detect what happens inside the nest.	
	
	https://stackoverflow.com/questions/29392650/python-using-a-multidimensional-multiprocessing-manager-list
	
### how to resolve data size conflict (for keras input)
	np.array(np.array(..)) does not work, need np.array([np.array(..)]) (i.e. each np.array only convert one layer of list)




### stuck at first epoch without progress bar?
	!!! do not use nn_thread (i.e. do not atempt to train in a subprocess, train directly in the main process)

### what is ETF all about?
	ETF does not have magical power, it is just a weighted average. i.e. some stock will return more than it and some will return less than it.
	1. given a stock, can I perdict if its return will be higher than ETF growth?
	2. given a stock, can I predict if it will grow or not?

### what range
	ETF return grabbing and computation
	comparison and decide buy short?

	i.e. return as a function of number of biggest cap companies we include
	
	what do we buy? what do we short (after range decided)?
		we cannot buy category or short category as that will give high correlation (and imagine predicting one wrong equals to predicting all wrong). Hence categorical appraoch should be avoided

### how to accelerate coding
	at each breakpoint, assume what you have something, output what is necessary for next breakpoint
###
	P(AB) = P(A)P(B)
	P(AB)/P(A) = P(B) ---> agree in B in \pi system ---> agree A in \sigma(\pi)
	
	two probability measure are equal in the entire \sigma(P) if they are equal on the \pi system? A probability measure is something that takes a set and output a probability

	try to prove this using BC lemma 
	w: |X_n(w)|/c_n > 1/n infinitely often  ---> = 1
	w: |X_n(w)|/c_n < 1/n for all n \geq N for some large N ---> = 0
	
	there are two coordinate, one w and another n.

### how to deal with BC lemma
	 w in limsup_{n \to \infty} E_n 
	 IF AND ONLY IF
	 w in E_n i.o.
	 
	 now shrinking notation
	 limsup_{n \to \infty} E_n 
	 IF AND ONLY IF
	 E_n i.o.
### how to use \pi system and \sigma condition in 280A HW4 P18?

	note that if two probability measure (i.e. function that takes in a set and output a value from 0-1)  on a \pi system, then they are equal everywhere in the \sigma algebra generated by that \pi system
	
	### what does independence in this case mean?
		it means A is indpendent from any set in the \ppi system

### infinite product is 0, but each term is not 0
	\prod(1-a_n) converges iff 
	ln(\prod (1-a_n)) = \sum_n ln(1-a_n) converges 

	now use e^{-x} \geq -x+1, which originates from e^x \geq x+1
### why favor larger ones?
	the larger the capitalization, the more likely that it will follow general trend (e.g. drop after overfrowth, increase after sharp drop)
??_? why not doing equal weight in CQA
	first, even doing equal weight, the adjustment procedure in convert_position is the same (sell old, buy new, remove large cap). There is no guarantee that it will take less number of actions than cap weighted ETF.

### breadth or depth or hybrid?
	org based rather than course based?
	is there a good heuristic?
	
	less weight given to less frequent, but for very frequent ones, reduce weight after familiar
	more weight given to people (older/more successful/more experience/more network)
	more weight given to direct contributables
	
	
	exploration on breadth
	
	### if were to be useful, must be target-based (e.g. act as filler) goal with ETF. What is the current ETF distribution?
		internship
		startup check
		
		advanced to candidacy (reading courses/committee search)
		courses
		
		project/filler (CQA, AWM, RFC events)
		exploration (Mfin, MBA, rady-org)
			https://rady.ucsd.edu/people/students/clubs/
		
		exploration -> decrease as familarity increase
### how to append list of rows to a dataframe
	k = pd.DataFrame([[1,2],[2,3]], columns = ["a", "b"])
	s = pd.DataFrame(new_ones, columns = k.columns)
	k.append(s)
	# only use ignore_index = True when columns are different but you do not want to merge rows?

### how to share strategy function
	### strategy(states):
		return action
		
	and now at higher level, historical direct compute reward, and live place_order and wait for reward.

### how to deal with BC lemma for P11
	1. limit implication with A -> B implies P(A) \leq P(B)
	2. B.C. lemma to deal with i.o.
	3. each rv, we can find a finite value such that tail probability is 1/2^n
	
### what are some cautions in trading algo
	1. strategy code can be shared in both live and historical
	2. algorithm must assume that there may be previously open positions (either by humans or algorithm itself), henec delta necessary
	

### CQA no-brain strategy	
	S&P 500, long top increase 41, short top decrease 41



	among ruseell, select the highest increase (or slope through polynomial regression) and highest decrease ones. Make a ETF out of it
	
	41 long, 41 short.
	
	1000
	
	etf
	russell 1000 ---> s&p 500
	russell 2000, small cap, highly volatile
	
	large long 40 + etf M-F
	ranked by slope*market_capitalization?
	large long 40 + large short 40 Friday-noon
	41 + 1 the rest 9 for adjustment.
	
	Friday
	
	based on market cap ranking/value or delta market cap ranking or market gain/loss?
	
	
	buy large, short small?
	among largest, buy category, short category?
### inverse of zip in python
	https://stackoverflow.com/questions/13635032/what-is-the-inverse-function-of-zip-in-python
		
### why is bar vs trade not important in terms of quality
	high, low, open, close are still random sample. Regardless which trade price we choose within the bar (or just 1 random price crawled from random interface), our sample rate is always 1 sample/min, and hence the quality of data does not change. 


### what are some of the search methods
	BFS/DFS

### how to acclerate coding
	pseudocode and scratch on one, then transfer the small ready-to-test chunks into another file
	

### whether to continue math PhD
	1. what are the problems that you actually want to solve
	2. are there methods that beat the current state-of-art? can someone in the department helps me find these new method?
	3. if there is not, find someone in other institutions who is willing to and transfer to there.


### how to deal with MLE for normal
	collecting term for constant/first order and second order
### which computation is better, short_moving_avg - long_moving_avg or short_moving_avg/long_moving_avg
	take - first (as MACD is doing -), but can change depending on experiement.

### how to chagne position based on pocket?
	current_price = ...
	quantity = (\pm ...)
	max_quantity = 
	
	in the end alpaca order in quantity (with conditional on fractionable)
	short/small as a test, persist/large to amplify reward signal

	current_pos = market_value
	current_pocket = cash + market_value
	current_percent = (market_value)/(cash + market_value)
	
	
	target_pos = current_pocket*target_percent
	number_to_buy_or_sell = (target_pos - current_pos)/share_price


### FlexMBA time
	Qual Analysis Tu	6:30p-9 1E107	
				Su	8:00a-10:30a 1E106
				Sa	2:30p-5:30p 1E106
	Managerial Econ Th	6:30p-9 1E107
					Sa 	8:00a-2 1E107
					### midterm 405
	Investment	Sa	8:00a-2:00p	3E107	
	

### what is the major source of load? or more precisely, what are the times where you feel "why do I have to do this?"
	encourage share notes with someone and social, similar interests networking, hiring
### why do people still need them after graduation?
	their new need, or their old habits from school
what kinds of note app are there?
	quickly snap pieces and also may write something
### what are the keys for 20D
	2, linear
	3, non-linear
	1, non-linear

### what does N(a,b) mean for normal random
	it means \mu = a, var = \sigma^2 = b (notice that it is NOT \sigma)

### how to make script portable (and immune from import error)?
	https://stackoverflow.com/questions/49117074/have-python-script-check-for-missing-modules-and-install-if-missing/49117143
### what are the major features
	seems not to have stackoverflow interface while forum's feature (e.g. announcement stuff)

	src of revenue: external bid-ask, school course website
	ways of taking: post questions+answers (make it suitable for assigments/quizzes as well) or just announcement/syllabus/files, comment, peer-reviewed grading, then either show score on gradescope or grade it at there, up vote-down vote (possibly with decay), tagging, latex and scannable, search, dashboard statistics/logistics/tasks/timeline (allow self add new events), screenshot to auto-create notes, visibility and time toggle (for exam/quizzes), automatically detect when there are text like assignment and quiz, shrinkable list based on time, hotness, tag etc.
	environment: note-taking 
	input to bid-ask, publish from instructors
	commpnay: allowed to see statistics and grades and send invitations
	stackoverflow (to replace piazza), to (partially) replace gradescope, and to replace canvas.
	stackvoerflow also as a notes taking and sharing website (using app)


### balance sheet vs income statement vs cashflow statement?
	balance: asset = liability + equity
		(what you have = what you borrow + what is reflected on stock market)
	income statement
		Net_earning(t) = Revenue(t) - Expenses(t) = retained_earning(t) - retained_earning(t-1)
	cashflow statement
		sum_cashflow(t) = in_cashflow(t) - out_cashflow(t) = cash(t) - cash(t-1)
		
	!! where retained earning and cash are items on the balance sheet. THat's how 3 items link together.	

### src need:
	questions, assignements, annoucement/syllabus, note-taking are separated, not knowing what to do/look at -> tag-based timeline/search on dashboard + tag/time/hotness Q&A with pemission settings + screenshot/markdown tool (+ peer-grading integrated with gradescope)
	desparate questions but no one answers <-> knowledgable people want some reward 
	students need to conveiently ask questions and get feedback/tutors, but there are not that many TA/grader <-> students/ex-TA can help but need some reward 
	
	student need good grade (extra credit) <-> verified way of getting extra
	instructor want students to engage <-> credit through participation

	why can't stackoverflow for team satisfy such need?
		screenshot
		permission/timing, 
		timeline and grade management
		
		
		can be easily extended from stack for team:
			Non Q&A post, e.g. announcement/syllabus
			reward/credit for participation
			school sso

	labor: cs students (CPT) from local campus	
### search with underscore does not work?
### install an input method

### mutable vs unmutable function para in python?
	https://stackoverflow.com/questions/575196/why-can-a-function-modify-some-arguments-as-perceived-by-the-caller-but-not-oth

### why can we feed old s-a-r?
	s-a-r is independent from time and neural network itself. For any neural netowkr, if you takae this action at this state, then here will be your reward

### how does multiprocessing share memory?
	https://stackoverflow.com/questions/5549190/is-shared-readonly-data-copied-to-different-processes-for-multiprocessing/5550156#5550156
### is probability = 1 a bad assumption? is smooth distribution bad assumption as well?	

	distribution should not exist, as real life is compsoed of pieces of info rather than a systematic drawer. More complicated models usually make worse performance
	
	computer performance = human performance + computational (search) power
	grab pieces from each model, but not excessively invest in any of them (e.g. new architecture, heavily-tweaked hyperparameter etc.)
	
	what can non-parametric statistics do?
	

	a pipe that takes in input and outputs a poset (in terms of likelihood) of the outcomes.

	one poset is better than the other, which they tehmselves form a poset. So we are basically finding best (upper bounds) of the posets
	
	ultimate objective: return? (need to consider volatility or not?)
	
	
### what are three forms of EMH	
	EMH: \omega information setd immediately incorporated into market price
	weak: \omega = past info
	semistrong \omega = past + present public info
	strong: \oemga = past + present public + present private info
	
	### how to disprove MEH in a study

	### what is the definition of not forecastable? shouldn't that mean each outcome has equal probability?
		
		EMH itself assumes that when all the information in \omega  are incorporated, expectation of change in stock prices is 0.
		disprove random walk = disprove EMH only when Q is not important
	
		product of Q and object prob = risk-neutral measure
	### hence disprove random walk = disprove EMH only when objective prob is approximately risk-neutral
	### how to compute Q there?
	### is there an example where it is demonstrated how to construct such tests?
	### ES-RNN
	### bootstrapping
	### residual of a time period boosted for next period?
### stationary vs white noise vs ergodic?
	https://www.asc.ohio-state.edu/de-jong.8/note1.pdf
	
	weakly stationary
		1. constant mean
		2, finite variance
		3. auto cov depending only on interval size
			There are two version, one from https://en.wikipedia.org/wiki/Stationary_process#Weak_or_wide-sense_stationarity 
			another from https://www.asc.ohio-state.edu/de-jong.8/note1.pdf
			
			Cov(s,t) = Cov(s-t, 0)
			Cov(s,t) = Cov(s+h, t+h) for any h
			
			first implies second as Cov(s+h, t+h) = Cov(s-t,0)
			second implies first if we let h = -t
	white noise
		https://stats.stackexchange.com/questions/335920/does-white-noise-imply-wide-sense-stationary?noredirect=1&lq=1
	
		1. zero mean (satisfy weak 1)
		2. finite variance (satisfy 2)
		3. autocov of any two $s,t$ equals to 0 (and therefore satisfy autocov condition)
		
		hence white noise implies stationary
			
	strong stationary	
		interval (not necesasrily consecutive) joint distribution is fixed along time
			1. interval = singleton implies constant mean
			2. interval = {X_{t_1}, X_{t_2}} implies auto cov condition
		
		
		
		
	### how is auto cov related to auto correlation?	
		https://en.wikipedia.org/wiki/Autocorrelation

### you cannot use something to predict itself?
	the cap trend and the number/category trend?

	event propagation needs time. Without time buffer, we cannot avoid EMH. (As you know, if you wait 3 days, any news about apple 3 days ago is already reflected in the price)
	
	### is there really something predicatable in trend, or it is just slightly better than noisy observations? i.e. is ES-RNN actually doing something or it is just that ES relives RNN from keep distracted by noises?
		https://eng.uber.com/m4-forecasting-competition/
		sure trend-only at t as input and trend-only at t+1 as output. But other than being better than a fixed coefficient (as in pure ES), does it do anything else?
		
		EMH: when you realize, you already lose (or win)

	i.e. can you compete in a way that do not only rely on the current slope you observe?

	### gnn and its relation with poset output?

### if there is a statistical model that proves to work, then can we use almost the same argument when we hybrid it with a neural network?

### How does a stop order and a stop limit order differ?
	https://money.stackexchange.com/questions/88719/why-use-a-stop-limit-order-instead-of-a-limit-order?newreg=777b3908cc514cb4ae6e26b11f55c9bb
	
	for example. Say current price is $40. 
	Limit order with $46: execute right now (as $40 < $46). But if the price goes down you lose money
	Stop-limit order with (sp: $45, lp: $46), wait until $45, and execute as long as it is under $46. This way, if the price drops you will not lose money as the order never execute.
	
	Hence limit buy if you predict price will go above limit. stop-limit if you predict price will go above limit PROVIDED it reaches the stop price.
	
### does it matter if the order is actually executed? the mdoel is more or less just a deep learning prediction model	
	the key problem is that in go, state + action implies next state. But here in stock market, state + action may have nothing to do with next state. Even if we add our total asset value as a state, it does not make much sense as our action policy is almost not influenced.
### how does hybrid of ES and RNN work?
	given previous trend, predict next trend using nn (rather than given previous observation, predict the next observation?)


### why do we need to deal with EMH? the process of incorporation of information is done by investors themselves. Hence if I do it faster than others, I can effectively ignore EMH?
	the ability to predict E(R_{t+1}) does not rule out EMH. We need to know Cov(R,Q) before possible contradiction

### how to acclerate coding
	make as many assumptions as possible (paid version, perfect always-on internet, correct starting time, database etc.), so that a running version can be produced as soon as possible
	
	get snippet of API and run them, if they work, then modify them into what you need rather than trying to write the entire thing yourself.
	
	figure out the pseduocode and replace it in place with python (pseudocode from high-level to low-level, replacement from low-level to high-level

### what are the major selling points of your product?
	imagine the main site is Q&A with ability to annoucement/syllabus/post
	imagine the ability to create easilt-managed notes with simple screenshots
	imagine the ability to resolve time-consuming problems with a little bit of money
	
	
### how to fetch data on the fly (free/paid version)
	# two things have to succeed
	# 1. latest bar
	# 2. no_gap
	
	# if latest bar not fetched, skip
	# if gap not fulfilled, skip
	
	# first part guarantee consecutiveness of temp_bars
	# second part guarantee no gap
	# the construction automatically ensure that gap and temp_bars are consecutive
	# hence if all satisfied and tradable, then we can safely compute
	
	# (i.e. start with assumming all consecutive till now, separately guarantee conseuctiveness of each part after adding this (arbitraily large) timestep)
	# note: we also automatically have always consecutiveness of database

	while true
		when not first_time and (cur_bar == temp_bars[-1]):
			do nothing
		elif not first_time and consecutive:
			fetch the latest bar
			if succeed: up_to_date = 1
		else:
			fetch the latest bar
			if succeed: up_to_date = 1
			temp_bars = [latest_bar]
			gap = [data_end + 1, latest_bar - 1]

		when gap exists (i.e. not None and data_end + 1 \leq latest_bar - 1):
			request historical_chunk to fill in gap
			if succeed:
				no_gap = true
			else:
				no_gap = false
			gap = None
		
		
		if up_to_date and no_gap and tradable now:
			compute (s,a)
			store into storage
			

### what low level functions are needed
	1. historical_chunk([a.b], session)
	2. latest_snapshot(session)

	
	
	
	
### difference between [key] and get(key)?
	[key] -> error and get(key) -> none

### use a database or csv?
	database unless extremely simple cases. If algorithm itself contains too many component (to foresee the need of database), use database first and reduce to csv later is necessary.
	
	
### why use bar rather than trade?
	trade api will return all individual trade. We need an interval based sampling and bar is more suitable for that
	
	

### how are bar data structured?
	they seem to be structured in a standard way, regardless where you are in 00:00-00:04, the latest bar (with timestamp 23:55) will always be 23:55-00:00
	
	
	
### difference between pandas column and index?
	df are matrices, index refers to row index. label themselves do not count towards index/non-emptiness
	
### how do we short?
	previous people's experience
	what shorting etf is profitable on market
	
### when to use pandas/list?
	use pandas when everything is ready (e.g. read from file/list) and do manipulation. Use a list for live accumulation of data. (This is similar to matlab matrix, where you do not keep appending stuff)

### what are some caution when dealing with http library?
	!! everything in and out has to be str, remember to convert str into json before manipulating response like a dictionary
	
	
### what is gradient boosting
	https://en.wikipedia.org/wiki/Gradient_boosting
	keep adding weak learners h_m to fit the residual, and expect the entire sum F_{m+1} to be a stronger learner than F_m
### ask innovation@ucsd.edu and jelena


### how to key
	Every time when you get stuck on a coding or math problem, the site that  Have you thought about extend it into a school platform?
	
	you constantly take notes for learning. Have you thought about arrange them in Q&A format and 
	
	desparate questions.
### what to do for the MGT 299?
	1. go into time series from DP
	2. go into reinforcement learning and attend all 254 from sicun
	3. go into market efficiency hypo from TA
	4. finally try to see if combination/hybrid of 1,2 is possible (along with any possible guarantee from 3)

### hybrid vs combination meaning in M4 paper?
	
	
### what can beat LSTM RL in time series forecasting?
	https://stats.stackexchange.com/questions/344258/neural-networks-vs-everything-else
	
	https://www.kaggle.com/c/optiver-realized-volatility-prediction/discussion?sort=votes
	https://www.kaggle.com/c/m5-forecasting-uncertainty/discussion?sort=votes
	https://www.kaggle.com/c/m5-forecasting-accuracy/discussion?sort=votes
	https://www.kaggle.com/c/jane-street-market-prediction/discussion?sort=votes
	
	
### what does trade_RL do?
	if model exists, load. Else create a new one.
	is_consecutive([a,b])
		if same day diff by one second
			return true
		elif different day by one is the end and the other is the beginning:
			return true
		else
			return false

	
	get_historical_data([data_base_end, current - 1])
		wait till 75 minutes from current - 1 (imagine not a trading day or not in trading range, wait 75 minutes does not harm, if in the trading range, then have to wait 75 minutes anyway (except 8:00, but complexify code for 1 minutes is unnecessary)
		request, write into database
		return true

	two thread:
		thread_1: once can_we_start becomes true, 
		
		every 30 seconds, if tradable and there is a new bar
			if the bar is consecutive:
				compute state, pass it through nn to get action and expected up/down size 
				if you take this action, on average how much confidence do you have?
				now put those into partial_storage_train or partial_storage_test with 7/3 split
			else
				get_historical_data([data_end, last_unfilled])
		else
			select a historical time
			compute state,action and put it in partial_storage_train or partial_storage_test with 7/3
			
		Check if reward of any in partial_storage (a list) is computable. Compute them and put them into storage_train/test
			
		thread_2: when there are enough stuff in the storage, train

### another key feature to mention
	related, as they are in site, can be integrated much more easily on side of the questions and dashboard

?? what are some applicable risk category
	https://www.dummies.com/business/fundraising/venture-capital/how-venture-capitalists-assess-risk-with-the-scorecard-method/


	1. market competitors.  if fail to be accepted by school, the risk increases (but not completely default as that is not the only source of revenue,).
	
	2. technological development. The standard interfaces (e,g. stackoverflow) already exists. Hence it is unlikely that the technology itself cannot be completed.
	
	3. audience: once developed and accpted, studetns (which is not a small market) will have to use it, just like they are forced to get used to Canvas as all instructors are using it. Furthermore, the note-taking services increase the likelihood that they continue to use it after school.
	
	4. financial: mainly developers (and they can even be in-school cs students) and servers cost. Hence does not require a large amount of monthly funds.
	
	5. people: math PhD. not need to worry about visa issues.
	
	6. other factors
		Canvas (and stackoverflow for team) for example is generally accepted as a usable platform. But they need massive amount of development to realize this idea without relying on third parties software.
		covid risk: not applicable as this is a virtual serivce (and this may be a significant advantage over other physical tech startup

### how to switch timezone in python
	1. datetime.now(timezone = ...)
	2. https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime

### relation between m and z estimator?
	every z is m. But not every m is z.

### how to compute fisher info
	use the property of expectation
	https://ani.stat.fsu.edu/~debdeep/Fisher.pdf
### what does P_\theta in vaan textbook mean?
	means E_\theta

### what is the flow of consistency/normality
	check example 5.40 (this uses general 5.7 for consistency and MLE specific (with fisher) 5.39
	
	### what if fisher (or fisher information matrix) does not exist?
		5.23 is basically a generalized version, but still require fisher
		
	### fisher information matrix
		https://arxiv.org/pdf/1705.01064.pdf
		!!! note that fisher is about a single piece of information, hence number of sample should never show up in the FIM.



### for cauchy, how to compute the distribution of sample mean?
	if same char function, then same distribution
	https://stats.stackexchange.com/questions/238246/what-is-the-distribution-of-sample-means-of-a-cauchy-distribution
### how to show MLE normality
	### QMD exists
		https://www.stat.berkeley.edu/~bartlett/courses/2013spring-stat210b/notes/22notes.pdf
	### liptschitz with k(x) and E(k^2) finite
		differentiable
### what is the notation for N(a,b)
	a is the mean, b is the variance (NOT the std)

### how to deal with MLE of uniform
	https://math.stackexchange.com/questions/49543/maximum-estimator-method-more-known-as-mle-of-a-uniform-distribution
	
	and the fact that x_max \leq \theta (and therefore \theta cannot be arbitrarily small)
	
	### but then how to deal with consistency?
		example 5.37, but how to jump from converging to exponential distribution to converge to 0 probability
		
		whenever we have max/min, we always use independece property to prove converging property
### what are common database query

	create table if not exist
		CREATE TABLE IF NOT EXISTS products (col_name col_type, col_name col_type,...)
		col_type can be INT, primary key,....
		
	insert (either replace/ognore) value or list of values into the table
		executemany() for list of values, otherwise syntax the same?
		INSERT OR REPLACE/IGNORE INTO table (col_1, col_2) VALUES ...

	obtain data with criteria from the table
		SELECT * FROM table WHERE col = ...
								col >  ...
	
	where ... can either be a string value (do not use %s due to injection attack), a ? (see below), or a subquery (e.g. that reutrns the max value in a column) or multiple of them connected by AND/OR.
		https://stackoverflow.com/questions/3727688/what-does-a-question-mark-represent-in-sql-queries	
	VALUES seem only appearing in INSERT statements	
		https://stackoverflow.com/questions/2251699/sqlite-insert-or-replace-into-vs-update-where


		
### is bar timestamped by start minute or end minute	
	bar timestamps are the bar start time
### what does alpaca.py do

	do we need to do real-time now? (if tradable AND data_ok, then we can, otherwise not)


	# fetch_historical_data into database
	if the previous trading bar is 75 min from now, 
		then (request) and ok.
	else
		wait 75 minute, request and ok.
	last_unfilled_trade = ...
	start = ...
	can_we_start = false
	async 1:
		start to query current point, if not trading, then just put NA
	async 2:
		fill [last_unfilled_trade, start] with NA
		keep querying [data_end, last_unfilled_trade] using historical API, once succeed, flush to database 
		can_we_start = true
		
		
		
		
### how to persuade
	try to correlate to what he wants to hear?
		
		

### difference between sql and sqlite?
	https://stackoverflow.com/questions/12666822/what-is-difference-between-sqlite-and-sql/12666833
### how to get through MLE sum?
	\sum_x x^2+\theta = 0 implies \bar{x^2} + \theta = 0
	
	
	no need to open site pages, q and a finished directly and flush to site.

### what is o_p(1) and O_p(1) in 281A?
	https://statisticaloddsandends.wordpress.com/2019/05/22/big-o_p-and-little-o_p-notation/
	
	small for ->_p 0 and big one for uniformly tight



### how to distribute time for the skills
	weighted ETF (instead of 1 or 0)

### can any forecasting model be used for earning money in the long term?
	any model, when most people start to use that model, the model becomes useless as the heuristic it generated is exploited too much
	
### how to place an order
	get total portfolio value
	get existing position
	get decision (a percentage)
	delta_pos = port*decision/limit_price - existing_pos
	
	!!! technically it should
	delta_pos = (port*decision - market_val_of_existing_pos)/limit price.
	
	But if our limit price is approximately the latest price, then we can use the first formula

### what is day trade? what is pattern day trader?
	a buy-sell within one day
	https://www.investor.gov/introduction-investing/investing-basics/glossary/pattern-day-trader
	
	
	
### what is a  p-value (and what is its relationship with significance level \alpha)
	https://en.wikipedia.org/wiki/P-value#Definition_and_interpretation
### how to handle backtesting
	share strategy but do not share running loop (along time). Now rather than checking is_tradable, directly jump to timestamp of next bar in the historical_data

### how to accelerate market coding
	always add a debug option to strategy function
	

### how to place_order in backtesting?
	balance is fixed. Hence the following
	
	existing_pos = existing_pos + delta_pos
	cash = balance - existing_pos*curbar["p"]
### how to deal with df? how to find the smallest index satisfying certian thing?
	df[label][index], not the other way around
	
	https://stackoverflow.com/questions/48719937/getting-typeerror-reduction-operation-argmax-not-allowed-for-this-dtype-when
	
	hence use first_valid_index on subdf instead.
	
	to pull out entire rows, use iloc[[]]
	https://stackoverflow.com/questions/46307490/how-can-i-extract-the-nth-row-of-a-pandas-data-frame-as-a-pandas-data-frame/46307819
### pd index of subdf
	does not change, remain the same as original df
	unless reset_index() after slicing
### efficient inefficient bellman?
	EMH does not exist if no one tries to beat the market
	EMH exist if everyone tries to beat the market


	# time value = information value
	# policy should action straetegy when inefficient and etf otherwise

### the more significant the event, the faster the information is incorporated?

cambo
### what is the practical difference between time series momentum and cross sectional momentum?
### still cannot find testing against EMH, should I even consider it before aiming for AI? READING DURING CLASS.
### Hassen efficently-inefficient -> can we measure how efficient it is rather than yes or no? If we can, can we formulate into a bellman problem?

### strategy update>
	if crossing line up/both up there but short is much higher than long
		buy
	if crossing line down/both down there but short is much lower than long
		short
		
	going out is generally more confident than going in or both out

### how to enable do not disturb (with exception of alarm) via adb?


### how to accelerate market coding?
	always assume live version at the beginning of API construction. i.e. everything is with respect to the current time.
	
	always assuming it is currently tradable. As if it is not tradable we do not need to make any decisions in live version anyway. After construciton, just make a is_tradable fucntion at code entry point.
	
	always assume rfc form (at the beginning of minute), because we can always convert one time at the top level and pass down (to avoid conversion from datetime obj to rfc in each level)
	
	always start by assuming a fixed ticker (e.g. "SPY")

	always standaized df into column "t" for time and column "p" for price within all subroutines
	
	The only overlap between live and backtesting version is the get_historical_bars(start,end) (and backtesting seems to only need that function). Even that, we never need to assume the end parameter to be the current time.

	use df for quit reading and data format conversion. MINIMIZE its usage in iteratively adding and slicing.

	skip month as and use year -> 252 day as measure conversion
	print out actual return against std etf return

	### hence how to construct previous_trading_minute?
		if is_tradable():
			get_calendar() to know open/close time
			if beginning of market
				fetch_historical_bars(data_end+1, today 00:00)
				return the last bar min
			else:
				return min-1
		else:
			return None
			
			
		non-live version
		if data_end < dt:
			tmp = fetch(data_end, dt)
			write tmp to database
			return tmp[-2]
		else
			return from database
	
### what is database injection attack
	when accepting user input string, if user input a string that contains a command and query simply take it as substring, then it will be executed.
	
	https://blog.sqreen.com/preventing-sql-injections-in-python/
	
### given start, end rfc, how to get_historical_bars deal with it?
	
	1. data_end does not exist (empty table):
		fetch and write in 1970-01-01 to end, now get stuff out
	if data_end exist:
		if data_end < start:
			fetch and write from data_end to end, now get stuff out
		if start < data_end < end
			fetch and write from data_end to end, now get stuff out
		if end < data_end 
			get stuff out
		# the first two cases being not sufficient data, the last case being all data already in database
### my team just does not want to work
### what to sepnd time?
		pre-criteria: has to have someone who is known to be more successful/experienced/knowledgable. (ie. ignore opportunistic events, e.g. MBA classes)
		
		(right, because given the same amount of time, we want rate of return to be higher.
		
		now among these events, place more weight on the ones where you can meet the same valued people over and over.. BUt after getting familar, can reduce the attendance rate.
		
		breadth only in terms of collecting events (including social/courses/project...) to attend. Whether to actually commit for an event, use the criteria above.
	
### why do we need prev_min
	because we need to make sure the data we end up with in live version is consecutive. There is no such need for historical_backtest because we can always
		if not exist in database
			get_historical_bar
			write into database
		else
			get from database

### how to show consistency and asymptotic normality of MLE?
	consistency 
		when there is analytical solution, probably use LLN
		otherwise 5.10
	normality
		when there is analytical solution, probably use CLT
		otherwise 5.39
			lipstchiz
			second moment
			fisher info
			
	Loss function, derivative = 0 gives MLE
	Fisher info
	aysmtotic normality based on Fisher

### what does it mean to say Poisson(1/\theta) in P1
	the pdf is \lambda^xe^{-\lambda}/x!, where \lambda is the parameter and x is the input. Note that the input is in \mathbb{N}
	

### finishing .xinitrc up
	1. 2560x1440 vs 1920x1080, check if need to add into sync.sh (or add a direct check into xinitrc
	2. geany minimum window size? has to be 900? 
		yes. xprop output min size 909.


### fix init.sh run on startup
	?

### 281A HW3
	?

### RL coding
	?? alpca -> database
	?? trading RL -> multithreading


### may need an answer, cannot find it? notes not centralized?
	linear sequence of Q&A, insert anywhere suitable

### what does fetchall return? how to extract stuff?
	array of rows, hence need double indices.
	
	
### derivative free method? does it help RL?

### when to check email (and any contact methods)?
	end of day. So that check and send can be combined?
	current list of contact:
		Facebook
		gmail 
		wechat
		discord

### how to execute that sqlite query in which create a table if not exist?
	alpaca.py ensure_full_data


	
### shortcut for rthought?


### what is market efficiency, how does it related to the deep learning models?
	under market efficiency hypothesis, all info are corporated immediately and therefore time series is not predictable to begin with. THerefore without testing, ML experiment can be critized.


### recursive explotit of self-estruct pattern? I know you know I know you are going to utilize this info?
			
		
			
### rotational indeterminacy?
			
			
### what is model instability and what are the approaches to deal with it?
	the population distribution varying over time
	1. we can model with more parameters 
	2. we can make the model most robust
			
			
### what are the differences between standard RNN and LSTM?:
	https://stats.stackexchange.com/questions/222584/difference-between-feedback-rnn-and-lstm-gru
	

### how to code quick?
	start with a working version (of a component), usually an example from the api we are using, then modify it to our need. DO not look at api and attempt to code something ourselves.
	

### how to ensure it is a library rather than a demo?
	check if it has pages of API definition. Even better, have example codes that just works after copy-paste.


### what is the difference between https://www.oxford-man.ox.ac.uk/wp-content/uploads/2020/06/Deep-Reinforcement-Learning-for-Trading.pdf and my setup?
	state: they have MACD and RSI, tehy also include normalized past return. Their past price is completely linear (i.e. past 60 observations)
	action: its action space only consists of [-1,0,1]
	reward: it depends on the utility function		
	network: similar as what we thought, 64-32 LSTM with Adam
	algroithm: same, using DQN





### how do I use weak law of large number on the question here? https://math.stackexchange.com/questions/243348/sample-variance-converge-almost-surely

	\frac{1/n} \sum_i Y_i \to E(Y), i.i.d is required so Y exists




### what stuff should I consider for stock market prediction
	alphastar: neural networks, self-play via reinforcement learning, multi-agent learning, and imitation learning
	
	combining max likelihood and MSE, i.e. imaging a reward function that has prob 0.3 for r_1, prob 0.4 for r_2 and prob 0.3 for r_3 given same state and action
	
	gnn, including when to produce new connection and neuron?

		

### what is the difference between python async-await and those in other languages?

		

### Wall street entrance (as of 2021/10/10)?
	commitee: Allan, DP, Jelena?, Sean?, ? -> 287, 402, 281, 257 -> time series hw?
	good intern track record
	resume
	project
	professional experience (TA)
	website
	
	leadership

	MATH PhD (or any other advanced degree)
	qual 200 -> rogalski OH
	advanced to candidacy -> to get full time of CPT
	reading and publish

### what is correlation?
	cov/sigma_1sigma_2, !!! note that we are not dividing by var
### how to quickly grab a field?
	1. go through standard graduate qualifying problems, just to get to know what subbranches are there.
	2. (recent) survey paper of particular branches and go through the links in the ref
	? or search highly cited professor and go from there?

