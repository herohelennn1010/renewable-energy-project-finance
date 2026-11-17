// One formula-driven build. Requires the bundled @oai/artifact-tool runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime=process.env.PROJECT_B_RUNTIME || path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies');
const require=createRequire(path.join(runtime,'node','entry.cjs'));
const {Workbook,SpreadsheetFile}=await import(require.resolve('@oai/artifact-tool'));
const input=JSON.parse(await fs.readFile(path.join(root,'model/inputs.json'),'utf8'));
const outdir=path.join(root,'model');
const previewdir='/tmp/project-b-model/previews';
await fs.mkdir(previewdir,{recursive:true});
const wb=Workbook.create(), grids={}, sheets={}, amap={};
const names=['Dashboard','Assumptions','Operations','Debt','Cash_Flow','Tax','Construction','Sensitivity','Sponsor','Inputs','Data','Sources','Checks','ReadMe'];
for(const name of names){sheets[name]=wb.worksheets.add(name);grids[name]={};}
function C(n){let s='';while(n){const k=(n-1)%26;s=String.fromCharCode(65+k)+s;n=Math.floor((n-1)/26);}return s;}
function idx(s){let n=0;for(const c of s)n=n*26+c.charCodeAt(0)-64;return n;}
function put(s,address,value){grids[s][address]=value;}
function F(s,c,r,expression){put(s,`${c}${r}`,'='+expression);}
function label(s,r,text,unit=''){put(s,'C'+r,text);put(s,'D'+r,unit);}
function A(n){if(!amap[n])throw Error('Unknown assumption '+n);return `'Assumptions'!$E$${amap[n]}`;}
function R(s,c,r){return `'${s}'!${c}${r}`;}
function CON(r){return `INDEX('Construction'!$E$${r}:$AN$${r},1,${A('months')})`;}
const excelDate=s=>(Date.parse(s+'T00:00:00Z')-Date.UTC(1899,11,30))/86400000;
const dateInputs=[];
input.assumptions.forEach((x,j)=>{
 const r=10+j;amap[x.name]=r;
 put('Assumptions','C'+r,x.name.replaceAll('_',' '));put('Assumptions','D'+r,x.assumption_id);
 let v=x.value;if(/^\d{4}-\d{2}-\d{2}$/.test(v)){v=excelDate(v);dateInputs.push(r);}else if(v!==''&&Number.isFinite(Number(v)))v=Number(v);
 put('Assumptions','E'+r,v);put('Assumptions','F'+r,x.unit);put('Assumptions','G'+r,'Hypothetical');
 put('Assumptions','H'+r,x.context_source_id);put('Assumptions','J'+r,x.rationale);
});
for(const [name,r,v,u,note] of [
 ['permanent_equity',81,53e6,'SGD','Frozen S$53m Phase 3 equity; no automatic stress-case equity plug.'],
 ['support_enabled',82,1,'0/1','Capped hypothetical completion support enabled.'],
 ['cure_enabled',83,0,'0/1','Operating cures disabled in baseline; this is an explicit switch.'],
 ['tolerance',84,.01,'SGD','Numerical reconciliation tolerance.']]){
 amap[name]=r;label('Assumptions',r,name.replaceAll('_',' '),u);put('Assumptions','E'+r,v);put('Assumptions','J'+r,note);
}
put('Assumptions','C4','Scenario number');put('Assumptions','E4',1);put('Assumptions','C5','Case selected');F('Assumptions','E',5,'CHOOSE(E4,"Base","Upside","Downside","Severe")');
const drivers=[
 ['merchant_multiplier',90,[1,1.2,.7,.6],'Sensitivity!$E$4'],
 ['yield_multiplier',91,[1,1.05,.9,.8],'Sensitivity!$E$5'],
 ['rate_shock',92,[0,-.005,.01,.02],'Sensitivity!$E$6'],
 ['opex_multiplier',93,[1,.95,1.1,1.2],'Sensitivity!$E$7'],
 ['capex_multiplier',94,[1,.95,1.1,1.2],null],
 ['delay_months',95,[0,0,3,6],null]];
for(const [n,r,values,sens] of drivers){
 amap[n]=r;label('Assumptions',r,n.replaceAll('_',' '));values.forEach((v,j)=>put('Assumptions',C(6+j)+r,v));
 const choice=`CHOOSE($E$4,F${r},G${r},H${r},I${r})`;
 F('Assumptions','E',r,`IF(CHOOSE($E$4,ISNUMBER(F${r}),ISNUMBER(G${r}),ISNUMBER(H${r}),ISNUMBER(I${r})),${choice}${sens?(n==='rate_shock'?'+':'*')+sens:''},NA())`);
}
['Active selection','Base','Upside','Downside','Severe'].forEach((v,j)=>put('Assumptions',C(j+5)+'88',v));
[.1,.2,.25,.25,.15,.05].forEach((w,j)=>{amap['stage'+j]=100+j;label('Assumptions',100+j,'Construction stage '+(j+1));put('Assumptions','E'+(100+j),w);});
const derived={months:110,actual_COD:111,repayment_quarters:112,original_EPC:113,actual_EPC:114,floating_rate:115,blended_rate:116,first_service_end:117,second_service_end:118,DSRA_coefficient:120,budget_uses:121};
Object.assign(amap,derived);for(const [n,r] of Object.entries(derived))label('Assumptions',r,n.replaceAll('_',' '));
F('Assumptions','E',110,`${A('construction_months')}+${A('delay_months')}`);
F('Assumptions','E',111,`EDATE(${A('base_COD')},${A('delay_months')})`);
F('Assumptions','E',112,`MAX(0,((YEAR(${A('fixed_maturity')})-YEAR(${A('actual_COD')}))*12+MONTH(${A('fixed_maturity')})-MONTH(${A('actual_COD')})+1)/3)`);
F('Assumptions','E',113,`${A('dc_capacity_mwp')}*1000*${A('EPC_cost_per_kwp')}`);
F('Assumptions','E',114,`${A('original_EPC')}*${A('capex_multiplier')}`);
F('Assumptions','E',115,`MAX(${A('benchmark_floor')},${A('benchmark_assumed')}+${A('rate_shock')})+${A('margin')}`);
F('Assumptions','E',116,`${A('hedged_fraction')}*(${A('swap_fixed_benchmark')}+${A('margin')})+(1-${A('hedged_fraction')})*${A('floating_rate')}`);
F('Assumptions','E',117,`EOMONTH(${A('actual_COD')},2)`);F('Assumptions','E',118,`EOMONTH(${A('actual_COD')},5)`);
F('Assumptions','E',120,`IF(${A('repayment_quarters')}>0,MIN(2,${A('repayment_quarters')})/${A('repayment_quarters')}+${A('blended_rate')}*((${A('first_service_end')}-${A('actual_COD')}+1)/365+IF(${A('repayment_quarters')}>1,(1-1/${A('repayment_quarters')})*(${A('second_service_end')}-${A('first_service_end')})/365,0)),0)`);
F('Assumptions','E',121,`${A('original_EPC')}*(1+${A('contingency_fraction')})+${A('development_cost')}+${A('loan_commitment')}*${A('upfront_fee')}+${A('IDC_budget')}+${A('initial_liquidity_budget')}+${A('DSRA_budget')}`);

for(const [r,text,v] of [[4,'Merchant price multiplier',1],[5,'Yield multiplier',1],[6,'Additional floating-rate shock',0],[7,'Opex multiplier',1]]){label('Sensitivity',r,text);put('Sensitivity','E'+r,v);}
put('Sensitivity','G4','Case selected');F('Sensitivity','I',4,"'Assumptions'!E5");
put('Sensitivity','C10','Tables exclude the planned replacement quarter. Full quarterly minimum is on Dashboard.');
put('Sensitivity','C11','Multipliers apply to the selected case; the two-input tables recalculate the same model.');

const conLabels={8:'Month number',9:'Start',10:'End',11:'Construction active',12:'COD funding month',20:'EPC spend fraction',24:'EPC cash cost',25:'Development',26:'Upfront loan fee',27:'Input GST paid',28:'GST refund',30:'Opening GST bridge',31:'GST bridge draw',32:'GST bridge repayment',33:'Closing GST bridge',34:'Unbridged GST cash cost',36:'Opening senior debt',37:'Opening project cash',38:'Permanent equity injection',39:'Cost before interest/reserve',40:'Interest year fraction',41:'COD reserve coefficient',42:'Uncapped required senior draw',43:'Senior draw after cap/longstop',44:'Construction cash interest',45:'Closing senior debt',46:'Undrawn commitment fee',47:'Initial DSRA funding',48:'Completion support draw',49:'Cumulative completion support',50:'Closing project cash',51:'Unfunded cash requirement',52:'Cash reconciliation',53:'Debt reconciliation',54:'GST bridge reconciliation',55:'Cumulative interest and fees',56:'Cumulative DSRA funding'};
for(const [r,l] of Object.entries(conLabels))label('Construction',r,l);
for(let j=0;j<6;j++)label('Construction',14+j,`Stage ${j+1} spend fraction`);
for(let m=1;m<=36;m++){
 const c=C(m+4),p=C(m+3),x=r=>`${c}${r}`,prev=r=>m>1?`${p}${r}`:'0';
 const e={8:`${m}`,9:`EDATE(${A('financial_close')},${x(8)}-1)`,10:`EOMONTH(${x(9)},0)`,11:`IF(${x(8)}<=${A('months')},1,0)`,12:`IF(${x(8)}=${A('months')},1,0)`};
 for(let j=0;j<6;j++)e[14+j]=`(MAX(0,MIN(1,6*${x(8)}/${A('months')}-${j}))-MAX(0,MIN(1,6*(${x(8)}-1)/${A('months')}-${j})))*${A('stage'+j)}`;
 Object.assign(e,{
 20:`SUM(${c}14:${c}19)`,24:`${A('actual_EPC')}*${x(20)}`,25:`IF(${x(8)}=1,${A('development_cost')},0)`,26:`IF(${x(8)}=1,${A('loan_commitment')}*${A('upfront_fee')},0)`,27:`(${x(24)}+${x(25)})*${A('GST_model_rate')}`,28:`IF(${x(8)}>${A('GST_recovery_months')},INDEX($E$27:$AN$27,1,MAX(1,${x(8)}-${A('GST_recovery_months')})),0)`,
 30:prev(33),31:`MIN(MAX(0,${A('sponsor_GST_bridge_cap')}-${x(30)}),MAX(0,${x(27)}-${x(28)}))`,32:`MIN(${x(30)},MAX(0,${x(28)}-${x(27)}))`,33:`${x(30)}+${x(31)}-${x(32)}`,34:`${x(27)}-${x(28)}-${x(31)}+${x(32)}`,
 36:prev(45),37:prev(50),38:`IF(${x(8)}=1,${A('permanent_equity')},0)`,39:`SUM(${c}24:${c}26)+${x(34)}`,40:`(${x(10)}-${x(9)}+1)/365*${x(11)}`,41:`${x(12)}*${A('DSRA_coefficient')}`,
 42:`MAX(0,(${x(39)}+${x(41)}*${x(36)}+${x(12)}*${A('initial_liquidity_budget')}-${x(37)}-${x(38)}+${x(36)}*${A('floating_rate')}*${x(40)}+(${A('loan_commitment')}-${x(36)})*${A('commitment_fee')}*${x(40)})/(1-(${A('floating_rate')}-${A('commitment_fee')})*${x(40)}/2-${x(41)}))`,
 43:`IF(AND(${x(11)}=1,${x(10)}<=${A('senior_draw_end')}),MIN(MAX(0,${A('loan_commitment')}-${x(36)}),${x(42)}),0)`,44:`(${x(36)}+${x(43)}/2)*${A('floating_rate')}*${x(40)}`,45:`${x(36)}+${x(43)}`,46:`MAX(0,${A('loan_commitment')}-${x(36)}-${x(43)}/2)*${A('commitment_fee')}*${x(40)}`,47:`${x(41)}*${x(45)}`,
 48:`IF(${A('support_enabled')}=1,MIN(MAX(0,${A('overrun_support_cap')}-${prev(49)}),MAX(0,${x(39)}+${x(44)}+${x(46)}+${x(47)}+${x(12)}*${A('initial_liquidity_budget')}-${x(37)}-${x(38)}-${x(43)})),0)`,49:`${prev(49)}+${x(48)}`,50:`${x(37)}+${x(38)}+${x(43)}+${x(48)}-${x(39)}-${x(44)}-${x(46)}-${x(47)}`,51:`MAX(0,${x(12)}*${A('initial_liquidity_budget')}-${x(50)})`,
 52:`${x(37)}+${x(38)}+${x(43)}+${x(48)}-${x(39)}-${x(44)}-${x(46)}-${x(47)}-${x(50)}`,53:`${x(36)}+${x(43)}-${x(45)}`,54:`${x(30)}+${x(31)}-${x(32)}-${x(33)}`,55:`${prev(55)}+${x(44)}+${x(46)}`,56:`${prev(56)}+${x(47)}`});
 for(const [r,expr] of Object.entries(e))F('Construction',c,r,expr);
}

const opLabels={8:'Operating quarter',9:'Start',10:'End',11:'Calendar days',12:'Operating year',13:'Asset operating',14:'Operating-year fraction',15:'Degradation factor',16:'Specific yield (kWh/kWp/year)',17:'Production before availability (MWh)',18:'Availability',19:'Curtailment',20:'Net generation (MWh)',22:'Contracted generation share',23:'PPA tariff (S$/MWh)',24:'Contracted revenue',25:'Merchant reference (S$/MWh)',26:'Merchant capture factor',27:'Merchant generation (MWh)',28:'Merchant revenue',29:'Total revenue',31:'O&M',32:'Roof access',33:'Insurance',34:'Administration',35:'Merchant settlement fee',36:'Total operating cost',37:'EBITDA',39:'Equipment replacement capex',40:'Decommissioning',41:'Lifecycle cash cost',43:'Receivables excluding GST',44:'Payables excluding GST',45:'Net operating working capital',46:'Change in working capital',47:'Net GST accrual',48:'Operating GST timing cash flow',49:'Cash income tax',50:'CFADS / FCF before debt service',52:'Organic quarterly DSCR',53:'DSCR excluding replacement',54:'Trailing 12-month minimum DSCR',55:'Forward 12-month minimum DSCR',56:'EBITDA / net cash interest'};
const debtLabels={8:'Operating quarter',9:'End',11:'Interest year fraction',12:'Scheduled service period',13:'Opening scheduled debt',14:'Scheduled principal',15:'Blended interest rate',17:'Net scheduled interest',18:'Scheduled debt service',19:'Closing scheduled debt',20:'Next two quarters DSRA target'};
const taxLabels={8:'Operating quarter',9:'End',11:'Opening book value',12:'Replacement additions',13:'Book depreciation',14:'Closing book value',16:'Capital allowances',17:'Net interest deduction',18:'Taxable profit before losses',19:'Opening tax losses',20:'Losses utilised',21:'Closing tax losses',22:'Current income tax accrual',23:'Cash income tax'};
const cfLabels={8:'Operating quarter',9:'End',10:'Opening operating cash',11:'CFADS',12:'Opening interest arrears',13:'Opening principal arrears',14:'Current interest due',15:'Current principal due',16:'Total debt payments due',17:'Cash before debt service',18:'Opening DSRA',19:'DSRA draw for debt service',20:'Limited equity cure draw',21:'Cash debt payments',22:'Interest paid',23:'Principal paid',24:'Closing interest arrears',25:'Closing principal arrears',26:'Actual senior debt incl. arrears',27:'Cash after debt service',28:'DSRA target',29:'DSRA replenishment',30:'Excess DSRA release',31:'Closing DSRA',32:'Cash before distributions',33:'Distribution lockup (1=yes)',34:'Distributions',35:'Closing operating cash',36:'Cumulative equity cure',37:'Unfunded operating cash need',38:'Unpaid debt service',39:'DSRA funding shortfall',40:'Cash reconciliation',41:'DSRA reconciliation',42:'Actual principal reconciliation'};
for(const [s,labels] of [['Operations',opLabels],['Debt',debtLabels],['Tax',taxLabels],['Cash_Flow',cfLabels]])for(const [r,l] of Object.entries(labels))label(s,r,l);
for(let q=1;q<=101;q++){
 const c=C(q+4),p=C(q+3),x=r=>`${c}${r}`,prev=r=>q>1?`${p}${r}`:'0',o=r=>R('Operations',c,r),d=r=>R('Debt',c,r),t=r=>R('Tax',c,r);
 const esc=`(1+${A('annual_escalation')})^(${x(12)}-1)*${A('opex_multiplier')}`;
 const op={8:`${q}`,9:`EDATE(${A('actual_COD')},3*(${x(8)}-1))`,10:`EOMONTH(${x(9)},2)`,11:`${x(10)}-${x(9)}+1`,12:`INT((${x(8)}-1)/4)+1`,13:`IF(${x(8)}<=${A('operating_life_years')}*4,1,0)`,14:`${x(11)}/(EDATE(${A('actual_COD')},${x(12)}*12)-EDATE(${A('actual_COD')},(${x(12)}-1)*12))*${x(13)}`,15:`(1-${A('annual_degradation')})^(${x(12)}-1)`,16:`${A('specific_yield')}*${A('yield_multiplier')}`,17:`${A('dc_capacity_mwp')}*${x(16)}*${x(14)}*${x(15)}`,18:A('availability'),19:A('curtailment'),20:`${x(17)}*${x(18)}*(1-${x(19)})`,22:`IF(${x(12)}<=${A('PPA_years')},${A('contracted_generation_share')},0)`,23:`${A('PPA_price')}*(1+${A('PPA_escalation')})^(${x(12)}-1)`,24:`${x(20)}*${x(22)}*${x(23)}`,25:`${A('merchant_reference')}*${A('merchant_multiplier')}*(1+${A('merchant_price_escalation')})^(${x(12)}-1)`,26:A('merchant_capture_factor'),27:`${x(20)}*(1-${x(22)})`,28:`${x(27)}*${x(25)}*${x(26)}`,29:`${x(24)}+${x(28)}`,
 31:`${A('dc_capacity_mwp')}*1000*${A('annual_OM_per_kwp')}*${x(14)}*${esc}`,32:`${A('dc_capacity_mwp')}*1000*${A('roof_lease_per_kwp')}*${x(14)}*${esc}`,33:`${A('actual_EPC')}*${A('insurance_fraction_EPC')}*${x(14)}*${esc}`,34:`${A('annual_admin')}*${x(14)}*${esc}`,35:`${x(27)}*${A('merchant_settlement_fee')}*${esc}`,36:`SUM(${c}31:${c}35)`,37:`${x(29)}-${x(36)}`,
 39:`IF(${x(8)}=${A('replacement_operating_year')}*4,${A('actual_EPC')}*${A('replacement_cost_fraction')}*(1+${A('annual_escalation')})^(${x(12)}-1),0)`,40:`IF(${x(8)}=${A('operating_life_years')}*4,${A('decommissioning_cost')}*(1+${A('annual_escalation')})^(${x(12)}-1),0)`,41:`SUM(${c}39:${c}40)`,43:`IF(${x(13)}=1,${x(29)}/${x(11)}*${A('receivable_days')},0)`,44:`IF(${x(13)}=1,${x(36)}/${x(11)}*${A('payable_days')},0)`,45:`${x(43)}-${x(44)}`,46:`${x(45)}-${prev(45)}`,47:`(${x(29)}-${x(36)}-${x(41)})*${A('GST_model_rate')}`,48:`((${x(29)}-(${x(43)}-${prev(43)}))-(${x(36)}-(${x(44)}-${prev(44)})+${x(41)}))*${A('GST_model_rate')}-${prev(47)}`,49:t(23),50:`${x(37)}-${x(49)}-${x(46)}-${x(41)}+${x(48)}`,
 52:`IF(${d(18)}>0,${x(50)}/${d(18)},"n.a.")`,53:`IF(AND(${d(18)}>0,${x(39)}=0),${x(52)},"n.a.")`,54:`IF(COUNT(${C(Math.max(1,q-3)+4)}52:${c}52)>0,MIN(${C(Math.max(1,q-3)+4)}52:${c}52),"n.a.")`,55:`IF(COUNT(${C(Math.min(101,q+1)+4)}52:${C(Math.min(101,q+4)+4)}52)>0,MIN(${C(Math.min(101,q+1)+4)}52:${C(Math.min(101,q+4)+4)}52),"n.a.")`,56:`IF(${d(17)}>0,${x(37)}/${d(17)},"n.a.")`};
 for(const [r,e] of Object.entries(op))F('Operations',c,r,e);
 const debt={8:o(8),9:o(10),11:`${o(11)}/365`,12:`IF(AND(${o(10)}<=${A('fixed_maturity')},${o(8)}<=${A('repayment_quarters')}),1,0)`,13:q===1?CON(45):prev(19),14:`IF(${x(12)}=1,IF(${o(8)}=${A('repayment_quarters')},${x(13)},MIN(${x(13)},${CON(45)}/MAX(1,${A('repayment_quarters')}))),0)`,15:A('blended_rate'),17:`IF(${x(12)}=1,${x(13)}*${x(15)}*${x(11)},0)`,18:`${x(14)}+${x(17)}`,19:`MAX(0,${x(13)}-${x(14)})`,20:q===101?'0':`SUM(${C(q+5)}18:${C(Math.min(101,q+2)+4)}18)`};
 for(const [r,e] of Object.entries(debt))F('Debt',c,r,e);
 const rep=`INDEX('Operations'!$E$39:$DA$39,1,${A('replacement_operating_year')}*4)`;
 const tax={8:o(8),9:o(10),11:q===1?A('actual_EPC'):prev(14),12:o(39),13:`IF(${o(13)}=1,${A('actual_EPC')}/(${A('book_depreciation_years')}*4)+IF(${o(8)}>${A('replacement_operating_year')}*4,${rep}/MAX(1,(${A('operating_life_years')}-${A('replacement_operating_year')})*4),0),0)`,14:`${x(11)}+${x(12)}-${x(13)}`,16:`IF(${o(8)}<=${A('tax_allowance_years')}*4,${A('actual_EPC')}/(${A('tax_allowance_years')}*4),0)+IF(AND(${o(8)}>${A('replacement_operating_year')}*4,${o(8)}<=(${A('replacement_operating_year')}+${A('tax_allowance_years')})*4),${rep}/(${A('tax_allowance_years')}*4),0)`,17:d(17),18:`${o(37)}-${x(16)}-${x(17)}-${o(40)}`,19:prev(21),20:`IF(${A('tax_loss_carryforward')}=1,MIN(${x(19)},MAX(0,${x(18)})),0)`,21:`IF(${A('tax_loss_carryforward')}=1,${x(19)}-${x(20)}+MAX(0,-${x(18)}),0)`,22:`MAX(0,${x(18)}-${x(20)})*${A('model_tax_rate')}`,23:`IF(${o(8)}>${A('tax_payment_lag_quarters')},INDEX($E$22:$DA$22,1,MAX(1,${o(8)}-${A('tax_payment_lag_quarters')})),0)`};
 for(const [r,e] of Object.entries(tax))F('Tax',c,r,e);
 const cf={8:o(8),9:o(10),10:q===1?CON(50):prev(35),11:o(50),12:prev(24),13:prev(25),14:d(17),15:d(14),16:`SUM(${c}12:${c}15)`,17:`${x(10)}+${x(11)}`,18:q===1?CON(56):prev(31),19:`MIN(${x(18)},MAX(0,${x(16)}-MAX(0,${x(17)})))`,20:`IF(${A('cure_enabled')}=1,MIN(MAX(0,${A('equity_cure_cap')}-${prev(36)}),MAX(0,${x(16)}-${x(17)}-${x(19)})),0)`,21:`MIN(${x(16)},MAX(0,${x(17)}+${x(19)}+${x(20)}))`,22:`MIN(${x(21)},${x(12)}+${x(14)})`,23:`MIN(${x(13)}+${x(15)},MAX(0,${x(21)}-${x(22)}))`,24:`${x(12)}+${x(14)}-${x(22)}`,25:`${x(13)}+${x(15)}-${x(23)}`,26:`${d(19)}+${x(25)}`,27:`${x(17)}+${x(19)}+${x(20)}-${x(21)}`,28:d(20),29:`MIN(MAX(0,${x(27)}-${A('initial_liquidity_budget')}),MAX(0,${x(28)}-(${x(18)}-${x(19)})))`,30:`MAX(0,${x(18)}-${x(19)}+${x(29)}-${x(28)})`,31:`${x(18)}-${x(19)}+${x(29)}-${x(30)}`,32:`${x(27)}-${x(29)}+${x(30)}`,
 33:`IF(OR(AND(ISNUMBER(${o(54)}),${o(54)}<${A('distribution_DSCR')}),AND(ISNUMBER(${o(55)}),${o(55)}<${A('distribution_DSCR')}),SUM(${x(24)}:${x(25)})>${A('tolerance')},${x(31)}<${x(28)}-${A('tolerance')},MAX('Construction'!$E$51:$AN$51)>${A('tolerance')},${A('actual_COD')}>${A('senior_draw_end')}),1,0)`,34:`IF(${x(33)}=0,MAX(0,${x(32)}-${A('initial_liquidity_budget')}),0)`,35:`${x(32)}-${x(34)}`,36:`${prev(36)}+${x(20)}`,37:`MAX(0,-${x(35)})`,38:`SUM(${x(24)}:${x(25)})`,39:`MAX(0,${x(28)}-${x(31)})`,40:`${x(10)}+${x(11)}+${x(19)}+${x(20)}+${x(30)}-${x(21)}-${x(29)}-${x(34)}-${x(35)}`,41:`${x(18)}+${x(29)}-${x(19)}-${x(30)}-${x(31)}`,42:`${CON(45)}-SUM($E$23:${c}23)-${x(26)}`};
 for(const [r,e] of Object.entries(cf))F('Cash_Flow',c,r,e);
}

const factsLookup={};
['Input ID','Period','Metric','Value (S$m)','Unit','Source','Printed locator','Entity scope'].forEach((h,j)=>put('Data',C(j+1)+'1',h));
input.facts.forEach((x,j)=>{const r=j+2;factsLookup[x.period+'|'+x.metric]=r;[x.input_id,x.period,x.metric,Number(x.value),x.unit,x.source_id,x.locator,x.entity_scope].forEach((v,k)=>put('Data',C(k+1)+r,v));});
['ID','Source','Publisher','Published','Period','URL','Printed locator'].forEach((h,j)=>put('Sources',C(j+1)+'1',h));
input.sources.forEach((x,j)=>[x.source_id,x.title,x.publisher,x.publication_date,x.financial_period,x.url,x.locator].forEach((v,k)=>put('Sources',C(k+1)+(j+2),v)));
const hist=['revenue','ebitda_management','finance_cost','ocf','ppe_ip_cashcapex','intangible_cashcapex','dividends_received','interest_paid','lease_principal_paid','debt_current','debt_noncurrent','cash_bs','equity'];
for(const [c,p] of [['E','FY2023'],['F','FY2024'],['G','FY2025']]){
 put('Sponsor',c+'8',p);hist.forEach((k,j)=>{label('Sponsor',j+10,k.replaceAll('_',' '),'S$m');F('Sponsor',c,j+10,`'Data'!D${factsLookup[p+'|'+k]}`);});
 for(const [r,l,e] of [[25,'Cash capex',`SUM(${c}14:${c}15)`],[26,'OCF less cash capex',`${c}13-${c}25`],[27,'Post-interest cash proxy',`${c}26+${c}16-${c}17-${c}18`],[28,'Gross debt excluding leases',`SUM(${c}19:${c}20)`],[29,'Net debt excluding leases',`${c}28-${c}21`],[30,'Net debt / EBITDA',`${c}29/${c}11`],[31,'EBITDA / finance costs',`${c}11/${c}12`]]){label('Sponsor',r,l);F('Sponsor',c,r,e);}
}
put('Sponsor','C35','FY2023 original; FY2024 restated. Cash-flow and continuing-revenue scopes differ.');
for(const [c,p] of [['I','1H2025'],['J','1H2026']]){put('Sponsor',c+'8',p);for(const [r,k] of [[10,'revenue'],[11,'ebitda_underlying'],[12,'finance_cost'],[13,'ocf']])F('Sponsor',c,r,`'Data'!D${factsLookup[p+'|'+k]}`);}
put('Sponsor','I16','Interim EBITDA is underlying.');put('Sponsor','I17','Do not annualise for acquired debt.');

const outputs={
8:['Senior commitment',A('loan_commitment'),'SGD'],9:['Actual debt drawn at COD',CON(45),'SGD'],10:['Permanent sponsor equity',A('permanent_equity'),'SGD'],
11:['Actual permanent uses',`${A('actual_EPC')}+${A('development_cost')}+${A('loan_commitment')}*${A('upfront_fee')}+${CON(55)}+${CON(56)}+${A('initial_liquidity_budget')}`,'SGD'],
12:['Construction interest and fees',CON(55),'SGD'],13:['Peak construction funding gap',"MAX('Construction'!$E$51:$AN$51)",'SGD'],14:['Completion support drawn',"SUM('Construction'!$E$48:$AN$48)",'SGD'],15:['Peak GST bridge',"MAX('Construction'!$E$33:$AN$33)",'SGD'],
16:['Minimum quarterly organic DSCR',"IF(COUNT('Operations'!$E$52:$DA$52)>0,MIN('Operations'!$E$52:$DA$52),\"n.a.\")",'x'],17:['Minimum DSCR excluding replacement',"IF(COUNT('Operations'!$E$53:$DA$53)>0,MIN('Operations'!$E$53:$DA$53),\"n.a.\")",'x'],18:['Quarters below covenant',`COUNTIFS('Operations'!$E$52:$DA$52,"<"&${A('minimum_DSCR')})`,'quarters'],19:['Peak unpaid debt service',"MAX('Cash_Flow'!$E$38:$DA$38)",'SGD'],20:['Actual senior debt at maturity',`INDEX('Cash_Flow'!$E$26:$DA$26,1,${A('repayment_quarters')})`,'SGD'],21:['Peak operating funding gap',"MAX('Cash_Flow'!$E$37:$DA$37)",'SGD'],22:['COD beyond construction longstop',`IF(${A('actual_COD')}>${A('senior_draw_end')},1,0)`,'1=yes'],23:['Commitment / planning funded cost',`${A('loan_commitment')}/${A('budget_uses')}`,'%'],24:['COD debt / first-year EBITDA',`IF(SUM('Operations'!$E$37:$H$37)>0,${CON(45)}/SUM('Operations'!$E$37:$H$37),"n.a.")`,'x'],25:['Minimum EBITDA / cash interest',"IF(COUNT('Operations'!$E$56:$DA$56)>0,MIN('Operations'!$E$56:$DA$56),\"n.a.\")",'x']};
for(const [r,[l,e,u]] of Object.entries(outputs)){label('Dashboard',r,l,u==='SGD'?'S$m':u);F('Dashboard','E',r,e);}
label('Dashboard',26,'Loan to value');put('Dashboard','E26','n.a.');put('Dashboard','G26','No independent asset valuation.');
label('Dashboard',28,'Numeric covenant result');F('Dashboard','E',28,`IF(ISNUMBER(E16),IF(E16<${A('minimum_DSCR')},"Covenant breach","No DSCR breach"),"No debt service")`);
put('Dashboard','C62','Full minimum includes replacement. Reserve draws and sponsor injections never increase CFADS.');
put('Dashboard','C63','The excluding-replacement result is diagnostic only, not the contractual covenant test.');
put('Dashboard','C32','Annual operating results (S$m; scheduled year-end debt)');
['Operating year','Revenue','CFADS','Debt service','Min quarterly DSCR','Ending debt'].forEach((v,j)=>put('Dashboard',C(j+3)+'34',v));
for(let y=1;y<=25;y++){
 const r=34+y,lo=C(5+(y-1)*4),hi=C(8+(y-1)*4);put('Dashboard','C'+r,y);
 for(const [c,e] of [['D',`SUM('Operations'!${lo}29:${hi}29)/1000000`],['E',`SUM('Operations'!${lo}50:${hi}50)/1000000`],['F',`SUM('Debt'!${lo}18:${hi}18)/1000000`],['G',`IF(COUNT('Operations'!${lo}52:${hi}52)>0,MIN('Operations'!${lo}52:${hi}52),"n.a.")`],['H',`'Debt'!${hi}19/1000000`]])F('Dashboard',c,r,e);
}
const checkrows=[
[8,'Construction cash difference',"MAX(MAX('Construction'!E52:AN52),-MIN('Construction'!E52:AN52))"],
[9,'Construction debt difference',"MAX(MAX('Construction'!E53:AN53),-MIN('Construction'!E53:AN53))"],
[10,'Operating cash difference',"MAX(MAX('Cash_Flow'!E40:DA40),-MIN('Cash_Flow'!E40:DA40))"],
[11,'DSRA roll-forward difference',"MAX(MAX('Cash_Flow'!E41:DA41),-MIN('Cash_Flow'!E41:DA41))"],
[12,'Actual principal difference',"MAX(MAX('Cash_Flow'!E42:DA42),-MIN('Cash_Flow'!E42:DA42))"],
[13,'Initial DSRA vs debt schedule',`${CON(56)}-SUM('Debt'!E18:F18)`],
[14,'Book value at asset-life end',"'Tax'!CZ14"],[15,'Construction GST bridge after run-off',"'Construction'!AN33"]];
for(const [r,l,e] of checkrows){label('Checks',r,l,'SGD');F('Checks','E',r,e);}
put('Checks','C18','Zero differences do not mean covenants pass. Breaches and funding gaps remain on Dashboard.');
put('Inputs','C8','Verified public observations are in Data and Sources; project assumptions are separate.');
const readme=[
'Independent educational simulation. No affiliation with DBS or Sembcorp; no actual loan or contracts.',
'Frozen information cutoff: 17 November 2026. Source facts, hypothetical inputs and formulas are separate.',
'Choose 1-4 in Assumptions E4. Active schedules and live sensitivity tables use that case.',
'Memo/CSV scenario comparisons are recalculated by switching this same build; there are no parallel hidden forecasts.',
'Neutral sensitivity inputs E4:E7 are 1, 1, 0, 1. Native tables change two inputs and restore the case.',
'Build money cells are SGD displayed in S$m. Sponsor/Data amounts are already S$m.',
'Blue inputs; green cross-sheet formulas; black same-sheet formulas and dashboard outputs.',
'Contingency and IDC are budget envelopes, not automatic expenses. Debt funds actual costs, not the entire commitment.',
'Construction is monthly; operation quarterly, with one run-off quarter for working capital and tax.',
'Construction draw, interest and initial DSRA are solved algebraically. Iteration is not enabled.',
'With a funding gap or missed longstop, operating results are conditional diagnostics, not proof of completion.',
'CFADS deducts replacement and decommissioning costs and GST timing. Reserve draws and cures are financing.',
'Full minimum DSCR includes replacement. The excluding-replacement figure is diagnostic only.',
'Cash retained by distribution lockups can fund payments without curing an organic DSCR breach.',
'Scheduled interest continues on the contractual path after a payment failure; arrears and actual principal are separately tracked.',
'This is not a default-workout model: penalty interest, acceleration and enforcement recoveries are not forecast.',
'Tax eligibility, future rates and GST recovery are hypothetical. Book depreciation and capital allowances are separate.',
'No LTV or independent valuation. Commitment / cost and actual debt are distinct.',
'FY2023 not recast; FY2024 restated. Interim earnings are not annualised against the acquired debt balance.',
'See validation report for calculation-engine and native Excel verification coverage.'
];readme.forEach((t,j)=>put('ReadMe','C'+(j+8),t));
for(const s of names)if(!['Data','Sources'].includes(s)){
 put(s,'C2',s==='Dashboard'?'Solar project finance and credit model':s.replaceAll('_',' '));
 if(!['Assumptions','Sensitivity'].includes(s)){put(s,'C4','Case selected');F(s,'E',4,"'Assumptions'!E5");}
}
for(const s of ['Construction','Operations','Debt','Cash_Flow','Tax'])put(s,'C6','Amounts in S$m unless a ratio or stated physical unit; underlying money values are SGD.');
// Author cells in blocks, then apply one consistent financial-model style.
const ink='#20354A',navy='#233F5D',green='#00804A',blue='#164ACC',amber='#FFF1C9';
const money='#,##0.0,,;(#,##0.0,,);"-"';
for(const s of names){
 const sheet=sheets[s],g=grids[s],byrow={};let maxr=0,maxc=0;
 for(const [address,v] of Object.entries(g)){const [,letters,rr]=address.match(/^([A-Z]+)(\d+)$/),r=+rr,c=idx(letters);maxr=Math.max(maxr,r);maxc=Math.max(maxc,c);(byrow[r]??={})[c]=v;}
 sheet.showGridLines=false;
 sheet.getRange(`A1:${C(maxc)}${maxr}`).format={font:{name:'Arial',size:10,color:ink},rowHeight:20,verticalAlignment:'center'};
 sheet.getRange(`A1:B${maxr}`).format.columnWidth=2;
 sheet.getRange(`C1:C${maxr}`).format.columnWidth=43;sheet.getRange(`D1:D${maxr}`).format.columnWidth=11;
 if(maxc>=5)sheet.getRange(`E1:${C(maxc)}${maxr}`).format.columnWidth=15;
 for(const [rs,values] of Object.entries(byrow)){
  const r=+rs,cs=Object.keys(values).map(Number),lo=Math.min(...cs),hi=Math.max(...cs);
  sheet.getRange(`${C(lo)}${r}:${C(hi)}${r}`).values=[Array.from({length:hi-lo+1},(_,j)=>{const v=values[lo+j];return typeof v==='string'&&v.startsWith('=')?null:v??null;})];
  const fc=cs.filter(c=>typeof values[c]==='string'&&values[c].startsWith('='));
  for(let i=0;i<fc.length;){let j=i;while(j+1<fc.length&&fc[j+1]===fc[j]+1)j++;const start=fc[i],end=fc[j];sheet.getRange(`${C(start)}${r}:${C(end)}${r}`).formulas=[Array.from({length:end-start+1},(_,k)=>values[start+k])];if(s!=='Dashboard')sheet.getRange(`${C(start)}${r}:${C(end)}${r}`).format.font.color=Array.from({length:end-start+1},(_,k)=>values[start+k]).some(f=>f.includes('!'))?green:'#111111';i=j+1;}
 }
 if(!['Data','Sources'].includes(s)){sheet.getRange('C2:L2').format.font={bold:true,size:14,color:ink};sheet.getRange('C2:L2').format.rowHeight=28;sheet.getRange('C3:L3').format.borders={bottom:{style:'thin',color:navy}};}
 if(['Operations','Debt','Cash_Flow','Tax','Construction'].includes(s)){
  sheet.getRange(`E8:${C(maxc)}${maxr}`).setNumberFormat(money);
  sheet.getRange(`E8:${C(maxc)}8`).setNumberFormat('0');
  const dateRows=s==='Operations'||s==='Construction'?[9,10]:[9];
  for(const r of dateRows)sheet.getRange(`E${r}:${C(maxc)}${r}`).setNumberFormat('d-mmm-yy');
  sheet.getRange(`C8:${C(maxc)}10`).format.fill=navy;sheet.getRange(`C8:${C(maxc)}10`).format.font.color='#FFFFFF';
  sheet.freezePanes.freezeRows(10);sheet.freezePanes.freezeColumns(4);
 }
 if(['Data','Sources'].includes(s)){sheet.freezePanes.freezeRows(1);sheet.getRange(`A1:${C(maxc)}1`).format={fill:navy,font:{bold:true,color:'#FFFFFF'}};sheet.getRange(`A1:A${maxr}`).format.columnWidth=25;sheet.getRange(`B1:C${maxr}`).format.columnWidth=28;sheet.getRange(`F1:H${maxr}`).format.columnWidth=65;}
}
// Units and meaningful totals, rather than full-cell grid borders.
for(const [s,rows] of [['Operations',[14,15,18,19,22,26]],['Debt',[11,15]],['Construction',[14,15,16,17,18,19,20,40,41]]])for(const r of rows)sheets[s].getRange(`E${r}:${s==='Construction'?'AN':'DA'}${r}`).setNumberFormat('0.0%');
for(const [s,rows] of [['Operations',[11,12,13]],['Debt',[12]],['Construction',[11,12]],['Cash_Flow',[33]]])for(const r of rows)sheets[s].getRange(`E${r}:${s==='Construction'?'AN':'DA'}${r}`).setNumberFormat('0');
for(const r of [16,17,20,23,25,27])sheets.Operations.getRange(`E${r}:DA${r}`).setNumberFormat('#,##0.0;(#,##0.0);"-"');
for(const r of [52,53,54,55,56]){sheets.Operations.getRange(`C${r}:DA${r}`).format.font.italic=true;sheets.Operations.getRange(`E${r}:DA${r}`).setNumberFormat('0.00"x";(0.00"x");"-"');}
for(const [s,rows] of [['Operations',[29,36,37,41,50]],['Debt',[18,19]],['Cash_Flow',[26,31,35,38]],['Construction',[45,50,51,55,56]]])for(const r of rows){const rr=sheets[s].getRange(`C${r}:${s==='Construction'?'AN':'DA'}${r}`);rr.format.fill='#EAF0F5';rr.format.font.bold=true;rr.format.borders={top:{style:'thin',color:'#B9C8D5'}};}
const ass=sheets.Assumptions;ass.getRange('E10:E84').format.font.color=blue;ass.getRange('E10:E84').format.fill=amber;ass.getRange('F90:I95').format.font.color=blue;ass.getRange('E90:E95').format.fill='#EAF0F5';ass.getRange('E4').format={fill:amber,font:{color:blue,bold:true},horizontalAlignment:'center'};ass.getRange('E4').dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:4}};
ass.getRange('J10:J84').format.columnWidth=96;ass.getRange('I1:I121').format.columnWidth=18;ass.getRange('C1:C121').format.columnWidth=34;ass.getRange('F88:I88').format={fill:navy,font:{color:'#FFFFFF',bold:true}};
for(const r of [...dateInputs,111,117,118])ass.getRange('E'+r).setNumberFormat('d-mmm-yy');
for(const x of input.assumptions){const r=amap[x.name];if(x.unit.startsWith('fraction'))ass.getRange('E'+r).setNumberFormat('0.0%');else if(x.unit==='SGD')ass.getRange('E'+r).setNumberFormat('#,##0');}
ass.getRange('E92:I92').setNumberFormat('0.0%');ass.getRange('E95:I95').dataValidation={rule:{type:'list',values:['0','3','6','9','12','15','18']}};
for(const s of names)if(!['Data','Sources','Sensitivity'].includes(s)){sheets[s].getRange(s==='Assumptions'?'E5':'E4').format={font:{color:green,bold:true},horizontalAlignment:'center',borders:{preset:'outside',style:'dotted',color:'#8D9BA8'}};}
sheets.Sensitivity.getRange('E4:E7').format={fill:amber,font:{color:blue}};sheets.Sensitivity.getRange('E6').setNumberFormat('0.0%');
sheets.Sensitivity.getRange('I4').format={font:{color:green,bold:true},horizontalAlignment:'center'};
const dash=sheets.Dashboard;dash.tabColor=navy;ass.tabColor='#5E7D9B';sheets.Inputs.tabColor='#B7C8D8';sheets.ReadMe.tabColor='#A6AAA9';
dash.getRange('E8:E25').setNumberFormat(money);dash.getRange('E16:E17').setNumberFormat('0.00"x";(0.00"x")');dash.getRange('E18').setNumberFormat('0');dash.getRange('E22').setNumberFormat('0');dash.getRange('E23').setNumberFormat('0.0%');dash.getRange('E24:E25').setNumberFormat('0.00"x"');dash.getRange('E8:E25').format.font.bold=true;
dash.getRange('G8:G28').format.columnWidth=50;dash.getRange('E28:H28').format.columnWidth=20;
dash.getRange('C34:H34').format={fill:navy,font:{color:'#FFFFFF',bold:true},wrapText:true,rowHeight:30};dash.getRange('D35:F59').setNumberFormat('0.0;(0.0);"-"');dash.getRange('G35:G59').setNumberFormat('0.00"x";(0.00"x")');dash.getRange('H35:H59').setNumberFormat('0.0;(0.0);"-"');
dash.getRange('E16').conditionalFormats.add('cellIs',{operator:'lessThan',formula:1.2,format:{fill:'#FCE4E1',font:{color:'#A32623',bold:true}}});
for(const r of [13,19,20,21,22])dash.getRange('E'+r).conditionalFormats.add('cellIs',{operator:'greaterThan',formula:.01,format:{fill:'#FCE4E1',font:{color:'#A32623',bold:true}}});
sheets.Checks.getRange('E8:E15').setNumberFormat('0.00;(0.00);0.00');sheets.Checks.getRange('E8:E15').format.font.color='#111111';sheets.Checks.getRange('E8:E15').conditionalFormats.addCustom('ABS(E8)>0.01',{fill:'#FCE4E1',font:{color:'#A32623',bold:true}});
sheets.Sponsor.getRange('E10:J29').setNumberFormat('#,##0;(#,##0);"-"');sheets.Sponsor.getRange('E30:G31').setNumberFormat('0.00"x"');sheets.Sponsor.getRange('C30:G31').format.font.italic=true;
sheets.Data.getRange(`D2:D${input.facts.length+1}`).setNumberFormat('#,##0');sheets.Data.getRange(`D2:D${input.facts.length+1}`).format.font.color=blue;
sheets.Data.getRange(`A1:A${input.facts.length+1}`).format.columnWidth=52;sheets.Data.getRange(`C1:C${input.facts.length+1}`).format.columnWidth=42;
sheets.Sources.getRange('B1:B26').format.columnWidth=56;sheets.Sources.getRange('C1:C26').format.columnWidth=33;sheets.Sources.getRange('D1:D26').format.columnWidth=16;
sheets.ReadMe.getRange('C8:C27').format.columnWidth=132;
// Two native editable charts bound to the annual table.
const chart=dash.charts.add('line',[dash.getRange('C34:C59'),dash.getRange('E34:E59'),dash.getRange('F34:F59')]);
chart.title='Annual CFADS and debt service (S$m)';chart.titleTextStyle.typeface='Arial';chart.titleTextStyle.fontSize=12;chart.setPosition('J8','S23');chart.legend={position:'top',textStyle:{typeface:'Arial'}};chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial'}};chart.yAxis={numberFormatCode:'0.0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial'}};
chart.series.items.forEach((s,j)=>s.line={fill:j?'#8D9BA8':'#255C88',style:'solid',width:2});
wb.recalculate();
const get=(s,r)=>sheets[s].getRange(r).values;
const snapshot=()=>Object.fromEntries(Object.entries(outputs).map(([r,[l]])=>[l,get('Dashboard','E'+r)[0][0]]));
console.log('Base',JSON.stringify(snapshot()));
await fs.writeFile(path.join(outdir,'formula_map.json'),JSON.stringify({assumptions:amap,outputs,grids},null,2));
const cases=[];
for(let c=1;c<=4;c++){ass.getRange('E4').values=[[c]];wb.recalculate();const result=snapshot();cases.push({case:['Base','Upside','Downside','Severe'][c-1],...result,first_year_generation:get('Operations','E20:H20')[0].reduce((a,b)=>a+b,0),replacement_capex:get('Operations','AZ39')[0][0],replacement_CFADS:get('Operations','AZ50')[0][0],replacement_DSCR:get('Operations','AZ52')[0][0],replacement_cash:get('Cash_Flow','AZ35')[0][0],checks:get('Checks','E8:E15').map(r=>r[0])});console.log('Case',cases.at(-1).case,JSON.stringify(result));}
ass.getRange('E4').values=[[1]];wb.recalculate();
await fs.writeFile(path.join(outdir,'scenario_results.json'),JSON.stringify(cases,null,2));
const headers=Object.keys(cases[0]).filter(k=>k!=='checks');const csvv=v=>typeof v==='string'?'"'+v.replaceAll('"','""')+'"':String(v);
await fs.writeFile(path.join(root,'data/processed/scenario_results.csv'),headers.map(csvv).join(',')+'\n'+cases.map(r=>headers.map(k=>csvv(r[k])).join(',')).join('\n')+'\n');
// Recalculate one-factor tests through the exact same workbook.
const stressTests=[];
for(const [name,cell,values] of [['merchant','E4',[.5,.7,1,1.2]],['yield','E5',[.7,.8,.9,1]],['rates','E6',[0,.01,.02,.03]],['opex','E7',[1,1.1,1.2,1.3]]]){
 for(const value of values){sheets.Sensitivity.getRange(cell).values=[[value]];wb.recalculate();stressTests.push({driver:name,value,...snapshot()});}
 sheets.Sensitivity.getRange(cell).values=[[name==='rates'?0:1]];
}
// Severe delay beyond longstop is a separately identified completion scenario.
const delayCell='I95',oldDelay=get('Assumptions',delayCell)[0][0];ass.getRange('E4').values=[[4]];ass.getRange(delayCell).values=[[12]];wb.recalculate();stressTests.push({driver:'severe_12_month_delay',value:12,...snapshot()});ass.getRange(delayCell).values=[[oldDelay]];ass.getRange('E4').values=[[1]];wb.recalculate();
await fs.writeFile(path.join(outdir,'stress_results.json'),JSON.stringify(stressTests,null,2));
// Distinguish the existing full-covenant breach, ordinary-quarter limits, and cash payment failure.
const breakpoints={full_covenant:'Already breached in the base replacement quarter; ordinary-quarter limits below do not cure it.'};
function bisect(cell,lo,hi,target,decreasing=true){
 for(let i=0;i<20;i++){
  const mid=(lo+hi)/2;stSet(cell,mid);const y=get('Dashboard','E17')[0][0];
  if((y>target)===decreasing)lo=mid;else hi=mid;
 }
 const value=(lo+hi)/2;stSet(cell,value);const result={input:value,ordinary_min_DSCR:get('Dashboard','E17')[0][0],full_min_DSCR:get('Dashboard','E16')[0][0]};stSet(cell,cell==='E6'?0:1);return result;
}
function stSet(cell,value){sheets.Sensitivity.getRange(cell).values=[[value]];wb.recalculate();}
// Yield DSCR rises with yield; reverse the bracket update used for adverse increases.
breakpoints.yield_at_ordinary_1_20=bisect('E5',.3,1,1.2,false);
breakpoints.opex_at_ordinary_1_20=bisect('E7',1,3,1.2,true);
breakpoints.rate_add_at_ordinary_1_20=bisect('E6',0,.15,1.2,true);
stSet('E4',0);breakpoints.zero_merchant_reference_ordinary_DSCR=get('Dashboard','E17')[0][0];stSet('E4',1);
let lastGood=1,firstBad=null;
for(let y=.95;y>=.35;y-=.05){stSet('E5',y);if(get('Dashboard','E19')[0][0]>1){firstBad=y;break;}lastGood=y;}
if(firstBad!==null){let lo=firstBad,hi=lastGood;for(let i=0;i<18;i++){let mid=(lo+hi)/2;stSet('E5',mid);if(get('Dashboard','E19')[0][0]>1)lo=mid;else hi=mid;}stSet('E5',(lo+hi)/2);breakpoints.yield_first_local_payment_failure={input:(lo+hi)/2,peak_unpaid:get('Dashboard','E19')[0][0],method:'First failure bracket in descending 5-point yield scan, then local bisection; cash-retention policy is piecewise.'};}stSet('E5',1);
// A diagnostic revised downside funding case: ordinary-quarter covenant only.
ass.getRange('E4').values=[[3]];let lo=53e6,hi=100e6;
for(let i=0;i<20;i++){const mid=(lo+hi)/2;ass.getRange('E81').values=[[mid]];wb.recalculate();if(get('Dashboard','E17')[0][0]>=1.2)hi=mid;else lo=mid;}
ass.getRange('E81').values=[[hi]];wb.recalculate();breakpoints.downside_ordinary_sizing_diagnostic={permanent_equity:hi,...snapshot(),qualification:'Full replacement-quarter covenant still fails. Not an approvable debt size or a completed restructuring.'};
ass.getRange('E81').values=[[53e6]];ass.getRange('E4').values=[[1]];wb.recalculate();
await fs.writeFile(path.join(outdir,'breakpoints.json'),JSON.stringify(breakpoints,null,2));
const engineTests=[];
function test(name,ok,detail=''){engineTests.push({name,status:ok?'PASS':'FAIL',detail});if(!ok)throw Error('Validation failed: '+name+' '+detail);}
const original=snapshot();
const unchangedActual=get('Sponsor','E10:G31');
ass.getRange('G90').values=[[null]];wb.recalculate();test('Blank unselected case does not alter base',Math.abs(get('Dashboard','E17')[0][0]-original['Minimum DSCR excluding replacement'])<1e-8);
ass.getRange('E4').values=[[2]];wb.recalculate();test('Selected missing input is exposed',String(get('Assumptions','E90')[0][0]).includes('#N/A'));
ass.getRange('G90').values=[[1.2]];ass.getRange('E4').values=[[1]];wb.recalculate();
ass.getRange('E'+amap.loan_commitment).values=[[0]];wb.recalculate();test('Zero senior loan makes DSCR not applicable',get('Dashboard','E16')[0][0]==='n.a.');
ass.getRange('E'+amap.loan_commitment).values=[[100e6]];wb.recalculate();
stSet('E5',0);test('Zero generation is not replaced by a healthy base',get('Operations','E20')[0][0]===0&&get('Dashboard','E16')[0][0]<0);stSet('E5',1);
ass.getRange('E'+amap.hedged_fraction).values=[[0]];stSet('E6',.02);const unhedged=get('Debt','E17')[0][0];ass.getRange('E'+amap.hedged_fraction).values=[[.7]];wb.recalculate();test('Hedge reduces exposed interest increase',get('Debt','E17')[0][0]<unhedged);stSet('E6',0);
test('Scenario and sensitivity changes leave verified history unchanged',JSON.stringify(get('Sponsor','E10:G31'))===JSON.stringify(unchangedActual));
test('Inputs restored to the original base',Math.abs(get('Dashboard','E9')[0][0]-original['Actual debt drawn at COD'])<.01&&get('Assumptions','E4')[0][0]===1);
await fs.writeFile(path.join(root,'validation/engine_tests.json'),JSON.stringify(engineTests,null,2));
// Preserve base-case detailed values for independent audit and memo generation.
const dump={};for(const s of ['Operations','Debt','Cash_Flow','Tax','Construction','Dashboard','Assumptions','Sponsor','Checks'])dump[s]={};
for(const s of Object.keys(dump))for(const a of Object.keys(grids[s]))dump[s][a]=get(s,a)[0][0];
await fs.writeFile(path.join(outdir,'base_values.json'),JSON.stringify(dump,null,2));
// Native two-variable tables use inputs physically located on this sheet.
const st=sheets.Sensitivity;
const nativeTables=[{range:'D15:I20',rowInput:'E4',columnInput:'E5',rows:[.7,.85,1,1.1,1.2],cols:[.8,.9,1,1.05,1.1],r:15,title:'Merchant price x yield: minimum DSCR excluding replacement'}, {range:'D25:I30',rowInput:'E6',columnInput:'E7',rows:[-.005,0,.01,.02,.03],cols:[.9,1,1.1,1.2,1.3],r:25,title:'Floating-rate shock x opex: minimum DSCR excluding replacement'}];
for(const table of nativeTables){
 st.getRange('C'+(table.r-2)).values=[[table.title]];st.getRange('D'+table.r).formulas=[["='Dashboard'!E17"]];
 st.getRange(`E${table.r}:I${table.r}`).values=[table.rows];st.getRange(`D${table.r+1}:D${table.r+5}`).values=table.cols.map(x=>[x]);
 st.dataTables.add(table.range,{rowInput:table.rowInput,columnInput:table.columnInput});
 st.getRange(`E${table.r+1}:I${table.r+5}`).setNumberFormat('0.00"x"');st.getRange(`E${table.r+1}:I${table.r+5}`).conditionalFormats.add('colorScale',{colors:['#E7B9B0','#F4F0E4','#BCD4C8'],thresholds:['min','50%','max']});
 st.getRange(`D${table.r}:I${table.r}`).format={fill:navy,font:{color:'#FFFFFF',bold:true}};
 st.getRange(`D${table.r+1}:D${table.r+5}`).setNumberFormat('0.00"x"');st.getRange(`E${table.r}:I${table.r}`).setNumberFormat(table.r===25?'0.0%':'0.00"x"');st.getRange('D'+table.r).setNumberFormat(';;;');
}
wb.recalculate();
await fs.writeFile(path.join(outdir,'sensitivity_values.json'),JSON.stringify({price_yield:get('Sensitivity','D15:I20'),rate_opex:get('Sensitivity','D25:I30')},null,2));
const expectedPY=get('Sensitivity','E16')[0][0];stSet('E4',.7);stSet('E5',.8);test('Native price/yield table agrees with direct model recalculation',Math.abs(expectedPY-get('Dashboard','E17')[0][0])<1e-8);stSet('E4',1);stSet('E5',1);
const expectedRO=get('Sensitivity','G29')[0][0];stSet('E6',.01);stSet('E7',1.2);test('Native rate/opex table agrees with direct model recalculation',Math.abs(expectedRO-get('Dashboard','E17')[0][0])<1e-8);stSet('E6',0);stSet('E7',1);
await fs.writeFile(path.join(root,'validation/engine_tests.json'),JSON.stringify(engineTests,null,2));
const inspection=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},maxChars:6000});
await fs.writeFile(path.join(root,'validation/formula_error_scan.ndjson'),inspection.ndjson);console.log('Error scan',inspection.ndjson.slice(0,1500));
const ranges={Dashboard:'C2:S28',Assumptions:'C88:I95',Operations:'C8:L37',Debt:'C8:L20',Cash_Flow:'C8:L42',Tax:'C8:L23',Construction:'C8:L26',Sensitivity:'C4:I30',Sponsor:'C8:J31',Inputs:'C2:H8',Data:'A1:F12',Sources:'A1:D12',Checks:'C8:F18',ReadMe:'C8:C18'};
for(const [s,r] of Object.entries(ranges)){
 try{const blob=await wb.render({sheetName:s,range:r,scale:1,format:'png'});await fs.writeFile(path.join(previewdir,s+'.png'),new Uint8Array(await blob.arrayBuffer()));}catch(e){console.log('Preview failed',s,e.message);}
}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(outdir,'renewable_project_finance.xlsx'));
console.log('Workbook exported.');
