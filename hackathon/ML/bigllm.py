from haystack.nodes import PreProcessor, PromptModel, PromptTemplate, PromptNode
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack import Pipeline
from haystack.nodes import BM25Retriever
from pprint import pprint
from json import loads, dumps
import numpy as np

HF_TOKEN ="your_hf_token_here"

with open('bigrag.json', 'r') as f:
    data = loads(f.read())

docs = [Document(content=str(data))]

processor = PreProcessor()
ppdocs = processor.process(docs)

docu_store = InMemoryDocumentStore(use_bm25=True)
docu_store.write_documents(ppdocs)
retriever = BM25Retriever(docu_store, top_k = 1)

qa_template = PromptTemplate(
    prompt =
    '''
    As the person in charge of mail distribution, your task is to direct emails to the right recipients.
    Use the context provided to determine the most fitting recipient(s) for the query.
    The context includes the organization's structure, departments, and teams.
    You can also use the description tag from the context to match the semantic meaning of the email.
    Your answer should be the id of the team(s) at the leaf node of the hierarchy to whom the query should be directed.
    Context: {join(documents)};
    Query: {query}
    Please respond in the following format: <x>
    where 'x' is the id of the leaf node.
    Your answer should ONLY INCLUDE THE ID
    '''
)


# qa_template = PromptTemplate(
#     prompt =
#     '''
#     DON'T ADD UNNECEASSARY INFO IN RESULT.
#     YOU MUST IDENTIFY TO WHOM THE QUERY SHOULD BE MAILED.
#     YOU CAN ADD MAILS IN RESULT IF YOU THINK THE INFO MUST BE SUBMITTED TO THEM
#     YOUR TASK IS TO IDENTIFY BEST SUITABLE OPTION(S) FROM CONTEXT FOR QUERY,
#     ANSWER IN COMMA SEPARATED VALUES WITHOUT ADDING SUGGESTIONS OR OPINIONS.
#     ANSWER MUST CONTAIN ALL THE MAILS IN LEAF NODE.
#     ANSWER MUST BE LEAF NODE.
#     RESULT CAN BE COMBINATION OF MULTIPLE LEAF NODES
#     Context: {join(documents)};
#     Prompt: {query}
#     '''
# )

prompt_node = PromptNode(
    model_name_or_path = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    api_key = HF_TOKEN,
    default_prompt_template=qa_template,
    max_length = 10,
    model_kwargs={"model_max_length":20000}
)

rag_pipeline = Pipeline()
rag_pipeline.add_node(component=retriever, name = 'retriever', inputs=['Query'])
rag_pipeline.add_node(component=prompt_node, name = 'prompt_node', inputs=['retriever'])

# q = f'''

# we want urgent support
# "entergy corporation and subsidiaries management's financial discussion and analysis annually , beginning in 2006 , if power market prices drop below the ppa prices ." 'accordingly , because the price is not fixed , the table above does not report power from that plant as sold forward after 2005 .' "under the ppas with nypa for the output of power from indian point 3 and fitzpatrick , the non-utility nuclear business is obligated to produce at an average capacity factor of 85% ( 85 % ) with a financial true-up payment to nypa should nypa's cost to purchase power due to an output shortfall be higher than the ppas' price ." 'the calculation of any true-up payments is based on two two-year periods .' 'for the first period , which ran through november 20 , 2002 , indian point 3 and fitzpatrick operated at 95% ( 95 % ) and 97% ( 97 % ) , respectively , under the true-up formula .' 'credits of up to 5% ( 5 % ) reflecting period one generation above 85% ( 85 % ) can be used to offset any output shortfalls in the second period , which runs through the end of the ppas on december 31 , 2004 .' 'entergy continually monitors industry trends in order to determine whether asset impairments or other losses could result from a decline in value , or cancellation , of merchant power projects , and records provisions for impairments and losses accordingly .' "marketing and trading the earnings of entergy's energy commodity services segment are exposed to commodity price market risks primarily through entergy's 50%-owned , unconsolidated investment in entergy-koch ." "entergy-koch trading ( ekt ) uses value-at-risk models as one measure of the market risk of a loss in fair value for ekt's natural gas and power trading portfolio ." 'actual future gains and losses in portfolios will differ from those estimated based upon actual fluctuations in market rates , operating exposures , and the timing thereof , and changes in the portfolio of derivative financial instruments during the year .' 'to manage its portfolio , ekt enters into various derivative and contractual transactions in accordance with the policy approved by the trading committee of the governing board of entergy-koch .' 'the trading portfolio consists of physical and financial natural gas and power as well as other energy and weather-related contracts .' 'these contracts take many forms , including futures , forwards , swaps , and options .' "characteristics of ekt's value-at-risk method and the use of that method are as follows : fffd value-at-risk is used in conjunction with stress testing , position reporting , and profit and loss reporting in order to measure and control the risk inherent in the trading and mark-to-market portfolios ." 'fffd ekt estimates its value-at-risk using a model based on j.p .' "morgan's risk metrics methodology combined with a monte carlo simulation approach ." 'fffd ekt estimates its daily value-at-risk for natural gas and power using a 97.5% ( 97.5 % ) confidence level .' "ekt's daily value-at-risk is a measure that indicates that , if prices moved against the positions , the loss in neutralizing the portfolio would not be expected to exceed the calculated value-at-risk ." 'fffd ekt seeks to limit the daily value-at-risk on any given day to a certain dollar amount approved by the trading committee .' "ekt's value-at-risk measures , which it calls daily earnings at risk ( de@r )

# '''

# q = "[\"( 1 ) on september 14 , 2012 , the company entered into a lease agreement for 186000 square feet of rentable space located in an office facility in canonsburg , pennsylvania , which serves as the company's new headquarters .\"\n 'the lease was effective as of september 14 , 2012 , but because the leased premises were under construction , the company was not obligated to pay rent until three months following the date that the leased premises were delivered to ansys , which occurred on october 1 , 2014 .'\n 'the term of the lease is 183 months , beginning on october 1 , 2014 .'\n \"the company shall have a one-time right to terminate the lease effective upon the last day of the tenth full year following the date of possession ( december 31 , 2024 ) , by providing the landlord with at least 18 months' prior written notice of such termination .\"\n \"the company's lease for its prior headquarters expired on december 31 , 2014 .\"\n '( 2 ) other operating leases primarily include noncancellable lease commitments for the company 2019s other domestic and international offices as well as certain operating equipment .'\n '( 3 ) unconditional purchase obligations primarily include software licenses and long-term purchase contracts for network , communication and office maintenance services , which are unrecorded as of december 31 , 2014 .'\n '( 4 ) the company has $ 17.3 million of unrecognized tax benefits , including estimated interest and penalties , that have been recorded as liabilities in accordance with income tax accounting guidance for which the company is uncertain as to if or when such amounts may be settled .'\n 'as a result , such amounts are excluded from the table above .'\n '( 5 ) other long-term obligations primarily include deferred compensation of $ 18.5 million ( including estimated imputed interest of $ 300000 within 1 year , $ 450000 within 2-3 years and $ 90000 within 4-5 years ) , pension obligations of $ 6.3 million for certain foreign locations of the company and contingent consideration of $ 2.8 million ( including estimated imputed interest of $ 270000 within 1 year and $ 390000 within 2-3 years ) .'\n 'table of contents .'] [\"contractual obligations the company's significant contractual obligations as of december 31 , 2014 are summarized below: .\"]"
# q = "im anish and i want to know about recruitment in Barclays"
# q = f"im facing technical problem with my computer, i need technical assistance"
# q = f"i am from tata and we want your services for cash flow"
# q = 'i want to get training on python'
# ans = rag_pipeline.run(query = q)
# print(type(ans['results']))
# for i in ans['results']:
#     print(i.strip())



def return_ans(q):
    try:
        ans = rag_pipeline.run(query = q)
        
        response = {
            "team": int(ans['results'][0].strip()),
            "status":200
        }
        print(response)
        return response
    except:
        response = {
            "team": ans['results'][0].strip(),
            "status":200
        }
        return response
        
