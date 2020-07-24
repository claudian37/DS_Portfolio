import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from gamblers_ruin import GamblersRuin

pio.templates.default='gridon'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
app.scripts.append_script({'external_url': mathjax })

colors = {
	'background': 'white',
	'header': 'black',
	'text1': 'black',
	'text2': '#3C85CC'
}


markdown_text1 = '''
Welcome! This web app is intended to illustrate the problem of the "gambler's ruin". Consider the following scenario: \n
You walk into a casino with an initial amount of $i, and you hope to increase your fortune to $N. You pick a gambling game where \n
your probability of success is p per round, and we assume that each round is independent and identically distributed (iid). \n
If you are successful that round, then one unit is added to your balance. If you lose that round, then one unit is removed \n
from your balance. The game ends when either your balance is $0 or reaches $N. What is your probability of winning/ reaching your goal of $N?
Play around with the numbers below to see how your probability of winning changes. \n
Conditions: N must be larger than i, and it is recommended to keep the number of games under 100 for faster results.
'''


markdown_text2 = '''
The section below shows your probability of winning as calculated by a formula, as well as your observed percentage of wins \n 
based on the number of games entered with margin of error for a 95% confidence interval. 
The graph shows the outcome of each game and the balance at every round.
'''

app.layout = html.Div([
		html.H1(children="Gambler's Ruin Demo", style={'color': colors['header'], 'padding': 30}),
		html.Div([dcc.Markdown(children=markdown_text1)], style={'padding-left': 50, 'display': 'display-inblock'}),
		html.Br(),
		html.Div(['Probability of Sucess for each round (p): ', 
				  dcc.Input(id='p_input', min=0, max=1, value='0.5', type='number')],
				  style={'padding': 5, 'padding-left':'100px', 'width':'50%', 'display': 'display-inblock', 'color': colors['text1']}),
		html.Div(['Initial Amount (i): ',
				  dcc.Input(id='i_input', value='10', type='number')],
				  style={'padding': 5, 'padding-left':'100px', 'display': 'display-inblock', 'color': colors['text1']}),
		html.Div(['Goal Amount (N): ', 
				  dcc.Input(id='N_input', value='20', type='number')],
				  style={'padding': 5, 'padding-left':'100px', 'color': colors['text1']}),
		html.Div(['Number of games: ',
			 	  dcc.Input(id='games_input', value='30', type='number')],
			 	  style={'padding': 5, 'padding-left':'100px', 'color': colors['text1'], 'backgroundColor': colors['background']}),
		html.Div([dcc.Loading(id='loading-1', type='circle', children=[html.Div(id="loading")]), 
				  html.Button(id='submit-button-state', n_clicks=0, children='Play')],
				  style={'padding':5, 'padding-left':'100px', 'margin':20, 'color': colors['text1']}),
		html.Div([dcc.Markdown(children=markdown_text2)], style={'padding-left': 50, 'display': 'display-inblock'}),
		html.Table([
			html.Tr([html.Td('Probability of winning (analytical solution): '), html.Td(id='prob')]),
			html.Tr([html.Td('Observed Percentage of Wins: '), html.Td(id='obs_wins')])],
			style={'padding': 5, 'margin-left': '100px', 'display': 'display-inblock', 'color': colors['text2']}),
		html.Div([dcc.Graph(id='gamble-graph')], style={'padding-left':'50px', 'backgroundColor': colors['background']})
])

# Inputs
@app.callback(
	[Output('loading-1', 'children'),
	 Output('gamble-graph', 'figure'),
	 Output('prob', 'children'),
	 Output('obs_wins', 'children')],
	[Input('submit-button-state', 'n_clicks')],
	[State('p_input', 'value'),
	 State('i_input', 'value'),
	 State('N_input', 'value'),
	 State('games_input', 'value')]
)

def update_graph(n_clicks, p_input, i_input, N_input, games_input):
	# Conditions: N > i, games < 100

	gr = GamblersRuin(p=float(p_input), i=int(i_input), N=int(N_input))
	df_outcome = gr.n_simulations(games=int(games_input))
	
	prob_win = gr.probability_win()

	perc_wins, perc_wins_ci = gr.observed_perc()
	obs_wins = str(round(perc_wins, 3)) + " \u00B1 " + str(round(perc_wins_ci, 3)) 

	fig = px.line(
				  df_outcome, x='round', y='balance', color='game',
				  range_x=[0,df_outcome['round'].max()+5], 
			 	  range_y=[0, int(N_input)+5]
			 	  )


	fig.update_layout(
					width=1000, 
					height=500,
					autosize=True
					)

	return True, fig, round(prob_win, 3), obs_wins


if __name__ == '__main__':
	app.run_server(debug=True)
