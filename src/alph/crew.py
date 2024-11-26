import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import BrowserbaseLoadTool

# Load environment variables
load_dotenv()
BROWSERBASE_API_KEY = os.getenv('BROWSERBASE_API_KEY')
BROWSERBASE_PROJECT_ID = os.getenv('BROWSERBASE_PROJECT_ID')

# Uncomment the following line to use an example of a custom tool
# from alph.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class Alph():
	"""Alph crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def crypto_alpha_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['crypto_alpha_researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			tools=[BrowserbaseLoadTool(BROWSERBASE_API_KEY, BROWSERBASE_PROJECT_ID)]
		)

	@agent
	def crypto_trading_advisor(self) -> Agent:
		return Agent(
			config=self.agents_config['crypto_trading_advisor'],
			verbose=True,
			tools=[BrowserbaseLoadTool(BROWSERBASE_API_KEY, BROWSERBASE_PROJECT_ID)]
		)

	@agent
	def crypto_portfolio_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['crypto_portfolio_manager'],
			verbose=True
		)

	@agent
	def crypto_risk_assessor(self) -> Agent:
		return Agent(
			config=self.agents_config['crypto_risk_assessor'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def research_alpha_opportunities(self) -> Task:
		return Task(
			config=self.tasks_config['research_alpha_opportunities'],
		)

	@task
	def advise_trade_bot_executions(self) -> Task:
		return Task(
			config=self.tasks_config['advise_trade_bot_executions'],
			output_file='report.md'
		)

	@task
	def manage_asset_portfolio(self) -> Task:
		return Task(
			config=self.tasks_config['manage_asset_portfolio'],
		)

	@task
	def assess_risks(self) -> Task:
		return Task(
			config=self.tasks_config['assess_risks'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Alph crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
