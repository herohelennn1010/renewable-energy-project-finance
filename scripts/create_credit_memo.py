"""Produce the five-page credit committee memo from validated model outputs."""
from pathlib import Path
import json,csv,html,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing,Line,String,PolyLine
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
b=load('model/base_values.json');cases=load('model/scenario_results.json');bp=load('model/breakpoints.json')
validation=load('validation/model_validation.json')
if validation['failed']:raise RuntimeError('Model checks must pass before memo creation')
base,up,down,severe=cases
with (ROOT/'docs/source_register.csv').open(newline='') as f:sources={r['source_id']:r for r in csv.DictReader(f)}
def m(n,dec=2):return f'{n/1e6:,.{dec}f}'
def ratio(n):return f'{n:.2f}x'
def money(n):return 'S$'+m(n)+'m'
def qcol(n):
 s=''
 while n:n,k=divmod(n-1,26);s=chr(65+k)+s
 return s
def val(s,r,q):return b[s][qcol(q+4)+str(r)]
def annual(s,r,y):return sum(val(s,r,q) for q in range((y-1)*4+1,y*4+1))
navy=colors.HexColor('#233F5D');ink=colors.HexColor('#233445');muted=colors.HexColor('#5C6F7F');red=colors.HexColor('#9B302B')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyB',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=7,textColor=ink))
styles.add(ParagraphStyle(name='SmallB',fontName='Helvetica',fontSize=8,leading=10.5,spaceAfter=5,textColor=muted))
styles.add(ParagraphStyle(name='TitleB',fontName='Helvetica-Bold',fontSize=19,leading=23,textColor=navy,spaceAfter=10))
styles.add(ParagraphStyle(name='HeadingB',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=navy,spaceBefore=9,spaceAfter=7))
styles.add(ParagraphStyle(name='CellB',fontName='Helvetica',fontSize=9,leading=12,textColor=ink))
styles.add(ParagraphStyle(name='CellWhite',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=colors.white))
styles.add(ParagraphStyle(name='DecisionB',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=red,spaceAfter=8))
P=lambda t,style='BodyB':Paragraph(t,styles[style])
W=A4[0]-84
story=[];md=[]
def section(title):story.append(P(title,'HeadingB'));md.extend(['','## '+title,''])
def text(t):story.append(P(t));md.append(t.replace('<b>','').replace('</b>',''))
def small(t):
 story.append(P(t,'SmallB'))
 md.append(re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>',lambda m:"["+html.unescape(m[2])+"]("+html.unescape(m[1])+")",t))
def tab(rows,widths,header=True):
 cells=[[P(str(x),'CellWhite' if header and i==0 else 'CellB') for x in row] for i,row in enumerate(rows)]
 t=Table(cells,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
 rules=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#C6D1DA'))]
 if header:rules += [('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#EFF3F6')])]
 t.setStyle(TableStyle(rules));story.extend([t,Spacer(1,6)])
 table_md=[]
 for i,row in enumerate(rows):
  table_md.append('| '+' | '.join(str(x).replace('<br/>',' ') for x in row)+' |')
  if header and i==0:table_md.append('| '+' | '.join('---' for _ in row)+' |')
 md.append('\n'.join(table_md))
def newpage():story.append(PageBreak())
def page_title(title):story.append(P(title,'TitleB'));md.extend(['','# '+title,''])

# Page 1.
page_title('Credit committee memorandum')
small('17 November 2026 | Independent project-finance case study | Information cutoff: 17 November 2026')
story.append(P('Recommendation: decline the request as currently structured','DecisionB'))
text('Evaluate a hypothetical <b>S$100m senior project-finance commitment</b> to Project B Solar Portfolio SPV, an assumed Sembcorp-sponsored Singapore commercial rooftop solar portfolio. This is an educational simulation. DBS and Sembcorp are not participants, and no real financing request or bank policy is represented.')
tab([['Proposed transaction','Hypothetical terms'],['Asset / borrower','120 MWp DC / 100 MWac across 60 assumed commercial rooftop sites; ring-fenced SPV.'],['Funding / repayment','S$153m planning envelope; S$53m permanent equity. Base actual uses '+money(base['Actual permanent uses'])+' and senior drawings '+money(base['Actual debt drawn at COD'])+'.'],['Dates / pricing','Close 1 Jan 2027; base COD 1 Jul 2028; fixed maturity 30 Jun 2043. 60 quarterly principal payments; illustrative 4.5% base interest, with 70% benchmark hedging after COD.'],['Revenue / recourse','80% as-generated production contracted for 20 years; 20% merchant. No full operating parent guarantee.']], [125,W-125])
section('Decision rationale')
text('<b>1. The original covenant fails in the base case.</b> Minimum organic quarterly DSCR is '+ratio(base['Minimum quarterly organic DSCR'])+' when year-12 replacement is paid, against the assumed 1.20x requirement. The excluding-replacement minimum of '+ratio(base['Minimum DSCR excluding replacement'])+' is a diagnostic and cannot replace the covenant test.')
text('<b>2. Downside cash payment failure is visible.</b> The combined downside requires '+money(down['Completion support drawn'])+' of hypothetical completion support and produces '+money(down['Peak unpaid debt service'])+' of temporary debt-service arrears with operating cures disabled. Eventual repayment at maturity does not erase that failure.')
text('<b>3. Completion funding is not robust.</b> The severe case exhausts S$20m of assumed completion support and retains a '+money(severe['Peak construction funding gap'])+' gap. COD also crosses the fixed longstop. Its operating forecasts are conditional diagnostics, not evidence that construction can finish.')
small('Model references: Dashboard E8:E25; Operations AZ39, AZ50, AZ52; Cash_Flow arrears and reserve schedules. All project-specific inputs and covenants are hypothetical. A balanced budget is not proof of bankability.')

# Page 2.
newpage();page_title('Sponsor financial assessment')
text('Sembcorp provides relevant operating scale and disclosed financial history. This assessment uses consolidated audited financial statements for annual history and the unaudited, unreviewed June 2026 update. These establish financial context, not an actual SPV equity or guarantee commitment. [S01-S04]')
tab([['S$ million unless stated','2023 original','2024 restated','2025'],['Revenue','7,042','6,417','5,799'],['Management EBITDA','1,789','1,734','1,520'],['Owner net profit, total','942','1,016','984'],['Operating cash flow','1,481','1,412','1,170'],['Net debt, excluding leases','6,487','7,800','7,847'],['Net debt / EBITDA','3.63x','4.50x','5.16x'],['EBITDA / finance costs','4.37x','4.66x','3.88x']], [W*.40,W*.20,W*.20,W*.20])
small('Sources: S01 printed pp10-15,124-134; S02 pp16-17,110-119. Management EBITDA is non-GAAP. FY2023 is not recast under the later investment-property accounting policy; FY2024 is restated. Cash-flow and continuing-revenue scopes can differ.')
section('Post-acquisition leverage matters')
text('June 2026 company-style net debt was <b>S$13,856m</b>, compared with S$7,847m at December 2025, following Alinta funding and debt consolidation. Interim operating cash flow fell to S$319m from S$672m in 1H2025. The full acquired debt balance is included, while reported interim earnings contain only one acquisition month. Do not simply annualise that earnings base. [S03,S04]')
text('Management separately reports annualised underlying pro-forma net debt / adjusted EBITDA of 5.3x and net debt / EBITDA of 6.1x, with stated environmental-certificate exclusions. These are issuer measures, not independent cash-coverage calculations. [S05, slide14]')
section('Liquidity and competing obligations')
text('The standalone parent disclosed S$101m of cash at June 2026, versus S$164m at December 2025. Consolidated cash of S$1,334m is not equivalent to freely upstreamable parent cash. June borrowings due within one year were S$1,420m; unprovided commitments totalled S$1,290m. Parent guarantees overlap group financing and should not be added mechanically to consolidated debt. [S03, pp13-15,29]')
text('For FY2025, OCF less cash PPE/investment-property and intangible capex was S$208m <b>before cash interest</b>. Adding dividends received and deducting cash interest and lease principal produces a S$55m cash-surplus proxy before acquisitions, equity investments and owner distributions. This is not the company-reported FCF measure. [S01; Sponsor schedule]')
text('Conclusion: require documented project equity and capped support rather than rely on reputation or consolidated size. The S$53m equity, S$15m GST bridge, S$20m completion support and S$10m cure capacity in this case are assumptions, not actual Sembcorp promises.')

# Page 3.
newpage();page_title('Project economics and repayment')
text('The baseline assumes S$1,100/kWp EPC cost; 1,250 kWh/kWp annual specific yield before separate 98% availability and 1% curtailment; 0.5% annual degradation; and S$180/MWh contracted pricing. Merchant sales use a hypothetical constant S$116.57/MWh historical reference with an 85% capture factor. The PPA tariff, resource assumptions and future prices are not verified project contracts or forecasts. [A001-A047; S14-S16]')
tab([['Base-case calculated metric','Result'],['First full operating-year generation',f'{base["first_year_generation"]/1000:,.2f} GWh'],['First-year revenue / CFADS',money(annual('Operations',29,1))+' / '+money(annual('Operations',50,1))],['Initial senior debt / DSRA',money(base['Actual debt drawn at COD'])+' / '+money(b['Construction']['V56'])],['Construction interest and commitment fees',money(base['Construction interest and fees'])],['Year-12 replacement / quarter CFADS',money(base['replacement_capex'])+' / '+money(base['replacement_CFADS'])],['Replacement-quarter DSCR / ending cash',ratio(base['replacement_DSCR'])+' / '+money(base['replacement_cash'])]], [W*.63,W*.37])
text('The S$153m funding envelope includes contingency and financing/reserve budgets. Actual cost-based draws are lower than the S$100m commitment: unused budget is not manufactured capex and unused loan commitment is not forced into cash. Actual initial DSRA and construction interest are formula-driven.')
section('Coverage and liquidity are different')
text('Base retained cash pays scheduled debt despite the replacement-quarter organic DSCR breach. The model deducts '+money(base['replacement_capex'])+' of replacement spending in CFADS, excludes reserve draws/cures from CFADS, and locks distributions using trailing and forward coverage tests. Base debt-service arrears are zero and senior debt is repaid by fixed maturity. The contractual breach still requires a revised, validated structure or an explicitly documented covenant treatment.')

# A compact vector chart built directly from the validated annual cash-flow values.
drawing=Drawing(W,155);left,bottom,cw,ch=34,27,W-48,105
maxval=25
for ytick in [0,10,20]:
 yy=bottom+ytick/maxval*ch;drawing.add(Line(left,yy,left+cw,yy,strokeColor=colors.HexColor('#D5DDE3'),strokeWidth=.4));drawing.add(String(1,yy-3,str(ytick),fontSize=8,fillColor=muted))
for ytick in [1,5,10,12,15,20,25]:drawing.add(String(left+(ytick-1)/24*cw-3,11,str(ytick),fontSize=8,fillColor=muted))
for s,r,color in [('Operations',50,colors.HexColor('#255C88')),('Debt',18,colors.HexColor('#909DA9'))]:
 pts=[]
 for year in range(1,26):pts.extend([left+(year-1)/24*cw,bottom+annual(s,r,year)/1e6/maxval*ch])
 drawing.add(PolyLine(pts,strokeColor=color,strokeWidth=1.5))
drawing.add(String(34,143,'Annual CFADS (blue) and scheduled debt service (grey), S$m',fontSize=8,fillColor=ink))
drawing.add(String(W-100,11,'Operating year',fontSize=8,fillColor=muted))
story.append(drawing)
small('After PPA expiry, all production becomes merchant. The baseline also shows a S$1.50m end-of-life operating funding gap after loan maturity, which requires lifecycle funding but is not a senior debt-service shortfall.')

# Page 4.
newpage();page_title('Stress tests and debt sizing')
text('Cases are deterministic assumptions, not probability estimates. Each comparison is calculated by changing the selector in the same linked model. Merchant shocks affect exposed sales; benchmark shocks affect all construction debt and the unhedged 30% after COD. Maturity and construction longstop stay fixed.')
tab([['Input change','Base','Upside','Downside','Severe'],['Merchant / yield','0% / 0%','+20% / +5%','-30% / -10%','-40% / -20%'],['Benchmark / opex','0 bp / 0%','-50 bp / -5%','+100 bp / +10%','+200 bp / +20%'],['EPC / delay','0% / 0 mo','-5% / 0 mo','+10% / 3 mo','+20% / 6 mo']], [W*.28,W*.18,W*.18,W*.18,W*.18])
tab([['Calculated output','Base','Upside','Downside','Severe*'],['Senior debt at COD, S$m']+[m(x['Actual debt drawn at COD']) for x in cases],['Full min quarterly DSCR']+[ratio(x['Minimum quarterly organic DSCR']) for x in cases],['Min DSCR excluding replacement']+[ratio(x['Minimum DSCR excluding replacement']) for x in cases],['Completion support, S$m']+[m(x['Completion support drawn']) for x in cases],['Unfunded construction, S$m']+[m(x['Peak construction funding gap']) for x in cases],['Peak debt arrears, S$m',m(base['Peak unpaid debt service']),m(up['Peak unpaid debt service']),m(down['Peak unpaid debt service']),'Conditional*']], [W*.36,W*.16,W*.16,W*.16,W*.16])
small('* Severe COD is 1 January 2029, just beyond the 31 December 2028 longstop, and completion is underfunded. Operational figures assume completion and cannot support approval. Zero conditional arrears would not cure the funding gap; blocked distributions also retain more cash in this case.')
section('Decision-useful sensitivities')
text('The full covenant already fails at baseline. Excluding only the planned replacement quarter, a generation multiplier of approximately '+f'{bp["yield_at_ordinary_1_20"]["input"]*100:.1f}%'+ ' reduces minimum DSCR to 1.20x. Even a zero merchant reference leaves this diagnostic at '+ratio(bp['zero_merchant_reference_ordinary_DSCR'])+' because 80% of production remains fixed-price contracted. These are conditional mathematical limits, not certified resource cases or market forecasts.')
text('Native two-variable tables show merchant price versus generation and floating-rate shock versus operating cost. They use the excluding-replacement diagnostic to make ordinary operating headroom readable; the full negative quarter remains visible on the dashboard. A higher interest denominator can make a negative DSCR appear less negative, so that ratio alone is not evidence of lower risk.')
section('Sizing does not solve the lifecycle event')
diag=bp['downside_ordinary_sizing_diagnostic']
text('A diagnostic downside rerun raises permanent equity to '+money(diag['permanent_equity'])+' and reduces actual debt to '+money(diag['Actual debt drawn at COD'])+' to reach 1.20x in ordinary quarters. The full minimum still fails and temporary arrears remain. This is <b>not an approvable debt size</b>. With the original quarterly CFADS definition and replacement during debt life, a lower loan alone cannot repair a negative replacement-quarter numerator.')

# Page 5.
newpage();page_title('Required restructuring and controls')
text('<b>Decision: reject the present structure and invite a revised submission.</b> This recommendation concerns the simulated structure and documented assumptions, not the creditworthiness of an actual Sembcorp transaction. No unconditional or conditional real-world approval is given.')
tab([['Requirement before reconsideration','Credit purpose'],['Fund the full asset lifecycle','Establish a legally controlled replacement/decommissioning reserve and validate its funding schedule. Agree a covenant basis that recognises funded lifecycle obligations without double-counting costs or inflating organic CFADS. Retain the full cash-flow view.'],['Re-size against the revised downside','Test every service period, payment liquidity, reserve adequacy and construction funding. Do not present the ordinary-quarter sizing diagnostic as final capacity. Cap draws at verified actual uses within the commitment.'],['Document sponsor obligations','Verify permanent equity and the separate GST/completion/cure facilities, their timing and caps. No unlimited support or freely upstreamable group cash assumption.'],['Resolve completion and offtake','Independent resource and engineering reports; site/roof rights, structural/grid review, relevant licences, EPC/O&M terms, signed PPAs, offtaker credit and concentration review. Any longstop waiver must be explicit.']], [W*.33,W*.67])
section('Illustrative covenant and security package')
text('Starting terms for a resubmission are minimum quarterly DSCR 1.20x and distribution tests at 1.30x, subject to an explicitly agreed lifecycle definition. Require a DSRA for the next two quarters of scheduled principal and net interest, 70% benchmark hedging and a 70% maximum commitment-to-defined-funded-cost ratio. These are hypothetical thresholds, not DBS policy. LTV is unavailable without a defensible valuation.')
text('Require share, asset and controlled-account security; assignments of PPAs, rooftop rights and insurance; direct agreements and step-in rights; monthly construction and quarterly operating/covenant reporting. Block distributions for breaches, arrears, reserve deficits or unresolved completion gaps. A cash cure cannot rewrite historical organic DSCR; any remedy and 30-day process needs explicit legal documentation.')
section('Evidence and limitations')
small('The workbook contains formula-linked cash flows, debt, tax and reserves, a source register and native sensitivity tables. '+str(validation['passed'])+' checks passed in the calculation engine and exported-file inspection. Native Microsoft Excel application recalculation was not independently verified. Post-default penalty interest, acceleration and enforcement recoveries are outside scope. There is no independent project valuation or actual contract/site diligence.')
refs=[('S01','Sembcorp Annual Report 2025, pp10-15,124-137'),('S02','Sembcorp Annual Report 2024, pp16-17,110-119'),('S03','1H2026 statements, pp2,13-15,22-23,29'),('S05','1H2026 results slides, slides13-15'),('S14','EMA indicative solar installation cost guidance'),('S16','EMC NEMS Market Report 2025, p20'),('S17','IRAS corporate tax rate'),('S20','IRAS GST rate')]
small('Primary references (click titles; complete locators and limits are in the workbook):')
for sid,title in refs:small(f'[{sid}] <link href="{html.escape(sources[sid]["url"],quote=True)}" color="#255C88">{html.escape(title)}</link>')

def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#CED8E0'));canvas.line(42,39,A4[0]-42,39)
 canvas.setFont('Helvetica',7.5);canvas.setFillColor(muted);canvas.drawString(42,27,'Independent educational simulation | Project B | 17 November 2026');canvas.drawRightString(A4[0]-42,27,f'{doc.page} / 5');canvas.restoreState()
pdf=ROOT/'memo/credit_committee_memo.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=50,title='Project B - Renewable Energy Credit Committee Memorandum',author='Independent case study')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
pages=len(PdfReader(pdf).pages)
if pages!=5:raise RuntimeError(f'Memo must be five pages; generated {pages}')
(ROOT/'memo/credit_committee_memo_source.md').write_text('\n\n'.join(md)+'\n',encoding='utf-8')
print('Created five-page credit memo and editable narrative source.')
if __name__=='__main__':pass
