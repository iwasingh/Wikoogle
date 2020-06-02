import unittest
import logging
from pathlib import Path
from searching.searcher import Searcher
from preprocessing.index import WikiIndex
from searching.fragmenter import Fragmenter, truncate
from parsing.compiler import Compiler
from query.expander import lca_expand

logging.basicConfig(level=logging.INFO)

DATA_FOLDER = Path(__file__).parent / 'data'


class TestSearcher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSearcher, self).__init__(*args, **kwargs)
        self.index = WikiIndex().get('__index')
        self.searcher = Searcher(self.index)

    def test_query_expansion(self):
        query = 'anarchism etymology'
        results = self.searcher.search(query)

    def test_snippet(self):
        results = self.searcher.search('anarkhia')
        results[0].snippet()

    def test_truncate(self):
        text = """Ascorbic acid is an organic compound with formula, originally called hexuronic acid. It is a white solid, but impure samples can appear yellowish. It dissolves well in water to give mildly acidic solutions. It is a mild redox|reducing agent."""
        print(truncate(text, 84))

    def test_fragmenter(self):
        text = """
{{About|the molecular aspects of ascorbic acid|information about its role in nutrition|Vitamin C}}
{{chembox
| Verifiedfields = changed
| Watchedfields = changed
| verifiedrevid = 477350783
| Name = {{sm|l}}-Ascorbic acid
| ImageFile = L-Ascorbic acid.svg
| ImageFile1 = Ascorbic-acid-from-xtal-1997-3D-balls.png
| IUPACName = (5''R'')-[(1''S'')-1,2-Dihydroxyethyl]-3,4-dihydroxyfuran-2(5''H'')-one
| OtherNames = Vitamin C
|Section1={{Chembox Identifiers
| IUPHAR_ligand = 4781
| UNII_Ref = {{fdacite|correct|FDA}}
| UNII = PQ6CK8PD0R
| SMILES1 = C([C@@H]([C@@H]1C(=C(C(=O)O1)O)O)O)O
| CASNo = 50-81-7
| ChEMBL_Ref = {{ebicite|changed|EBI}}
| ChEMBL = 196
| CASNo_Ref = {{cascite|changed|??}}
| EINECS = 200-066-2
| ChemSpiderID_Ref = {{chemspidercite|changed|chemspider}}
| ChemSpiderID = 10189562
| PubChem = 5785
| KEGG_Ref = {{keggcite|correct|kegg}}
| KEGG = D00018
| ChEBI_Ref = {{ebicite|changed|EBI}}
| ChEBI = 29073
| StdInChI_Ref = {{stdinchicite|changed|chemspider}}
| StdInChI = 1S/C6H8O6/c7-1-2(8)5-3(9)4(10)6(11)12-5/h2,5,7-10H,1H2/t2-,5+/m0/s1
| StdInChIKey_Ref = {{stdinchicite|changed|chemspider}}
| StdInChIKey = CIWBSHSKHKDKBQ-JLAZNSOCSA-N
| SMILES = OC=1C(OC(=O)C=1O)[C@@H](O)CO
 }}
|Section2={{Chembox Properties
| C=6 | H=8 | O=6
| Appearance = White or light yellow solid
| Density = 1.65{{nbsp}}g/cm<sup>3</sup>
| MeltingPtC = 190 to 192
| MeltingPt_notes = decomposes 
| Solubility = 330{{nbsp}}g/L
| Solubility1 = 20{{nbsp}}g/L
| Solvent1 = ethanol
| Solubility2 = 10{{nbsp}}g/L
| Solvent2 = glycerol
| Solubility3 = 50{{nbsp}}g/L
| Solvent3 = propylene glycol
| SolubleOther = Insoluble in [[diethyl ether]], [[chloroform]], [[benzene]], [[petroleum ether]], [[oil]]s, [[fat]]s
| pKa = 4.10 (first), 11.6 (second)
  }}
|Section6={{Chembox Pharmacology
| ATCCode_prefix = A11
| ATCCode_suffix = GA01
| ATC_Supplemental = {{ATC|G01|AD03}}, {{ATC|S01|XA15}}
}}
|Section7={{Chembox Hazards
| ExternalSDS = [http://hazard.com/msds/mf/baker/baker/files/a7608.htm JT Baker]
| NFPA-H = 1
| NFPA-F = 1
| NFPA-R = 0
| MainHazards =
| FlashPt =
| AutoignitionPt =
| LD50 = 11.9{{nbsp}}g/kg (oral, rat)<ref>[https://web.archive.org/web/20070209221915/http://physchem.ox.ac.uk/MSDS/AS/ascorbic_acid.html Safety (MSDS) data for ascorbic acid]. [[University of Oxford]]</ref>
  }}
}}

'''Ascorbic acid''' is an [[organic compound]] with formula {{chem|C|6|H|8|O|6}}, originally called '''hexuronic acid'''. It is a white solid, but impure samples can appear yellowish.  It dissolves well in water to give mildly acidic solutions.  It is a mild [[redox|reducing agent]].

Ascorbic acid exists as two [[enantiomer]]s (mirror-image [[isomer]]s), commonly denoted "{{sm|l}}" (for "levo") and "{{sm|d}}" (for "dextro"). The {{sm|l}} isomer is the one most often encountered: it occurs naturally in many foods, and is one form ("[[vitamer]]") of [[vitamin C]], an essential nutrient for humans and many animals. Deficiency of vitamin C causes [[scurvy]], formerly a major disease of sailors in long sea voyages. It is used in as a [[food additive]] and a [[dietary supplement]] for its [[antioxidant]] properties. The "{{sm|d}}" form can be made via [[chemical synthesis]] but has no significant biological role.

==History==
<!--Please try to restrict this section to the history of the chemistry of the compound.  The medical aspects belong more properly to the [[scurvy]] and [[vitamin C]] articles.-->
The [[scurvy|antiscorbutic]] properties of certain foods were demonstrated in the 18th century by [[James Lind]]. In 1907, [[Axel Holst]] and [[Theodor Frølich]] discovered that the antiscorbutic factor was a water-soluble chemical substance, distinct from the one that prevented [[beriberi]]. Between 1928 and 1932, [[Albert Szent-Györgyi]] isolated a candidate for this substance, which he called it "hexuronic acid", first from plants and later from animal adrenal glands. In 1932 [[Charles Glen King]] confirmed that it was indeed the antiscorbutic factor.

In 1933, sugar chemist [[Norman Haworth|Walter Norman Haworth]], working with samples of "hexuronic acid" that Szent-Györgyi had isolated from [[paprika]] and sent him in the previous year, deduced the correct structure and optical-isomeric nature of the compound, and in 1934 reported its first synthesis.<ref>[https://profiles.nlm.nih.gov/WG/Views/Exhibit/narrative/szeged.html Story of Vitamin C's chemical discovery]. Profiles.nlm.nih.gov. Retrieved on 2012-12-04.</ref><ref>{{Cite book | last = Davies  | first = Michael B.  | last2 = Austin  | first2 = John  | last3 = Partridge  | first3 = David A. | name-list-format = vanc | title = Vitamin C: Its Chemistry and Biochemistry  | publisher = The Royal Society of Chemistry  | year = 1991  | page = 48  | isbn = 0-85186-333-7}}
</ref> In reference to the compound's antiscorbutic properties, Haworth and Szent-Györgyi proposed to rename it "a-scorbic acid" for the compound, and later specifically {{sm|l}}-ascorbic acid.<ref>{{citation | first1 = Joseph Louis | last1 = Svirbelf | first2 = Albert | last2 = Szent-Györgyi | name-list-format = vanc | authorlink2 = Albert Szent-Györgyi | url = https://profiles.nlm.nih.gov/WG/B/B/G/W/_/wgbbgw.pdf | title = The Chemical Nature Of Vitamin C | journal = Science | volume = 75 | issue = 1944 | pages = 357–8 | date = April 25, 1932| bibcode = 1932Sci....75..357K | doi = 10.1126/science.75.1944.357-a | pmid = 17750032 }}. Part of the [[National Library of Medicine]] collection. Accessed January 2007</ref>  Because of their work, in 1937 the [[Nobel Prize]]s for chemistry and medicine were awarded to Haworth and Szent-Györgyi, respectively.

==Chemical properties==

===Acidity===
Ascorbic acid is a [[vinylogous]] [[carboxylic acid]] and forms the [[ascorbate]] anion when deprotonated on one of the hydroxyls. This property is characteristic of [[reductone]]s: [[enediol]]s with a [[carbonyl]] group adjacent to the enediol group, namely with the  group –C(OH)=C(OH)–C(=O)–.  The ascorbate anion is stabilized by electron delocalization that results from [[resonance (chemistry)|resonance]] between two forms:

:[[File:Ascorbate resonance.png|400px]]

For this reason, ascorbic acid is much more acidic than would be expected if the compound contained only isolated hydroxyl groups.

===Salts===
The ascorbate anion forms [[salt (chemistry)|salts]], such as [[sodium ascorbate]], [[calcium ascorbate]], and [[potassium ascorbate]].

===Esters===
Ascorbic acid can also react with organic acids as an [[alcohol (chemistry)|alcohol]] forming [[ester]]s such as [[ascorbyl palmitate]] and [[ascorbyl stearate]].

===Nucleophilic attack===
[[Nucleophile|Nucleophilic attack]] of ascorbic acid on a proton results in a 1,3-diketone: 

:[[Image:Ascorbic diketone.png]]

===Oxidation===
[[File:L-Semidehydroascorbinsäure.svg|right|thumb|220px|Semidehydroascorbate acid radical]]
[[File:Dehydroascorbic_acid_2.svg|right|thumb|220px|Dehydroascorbic acid]]
The ascorbate ion is the predominant species at typical biological pH values. It is a mild [[reducing agent]] and [[antioxidant]]. It is oxidized with loss of one electron to form a [[radical (chemistry)|radical]] [[cation]] and then with loss of a second electron to form [[dehydroascorbic acid]]. It typically reacts with oxidants of the [[reactive oxygen species]], such as the [[hydroxyl radical]].

Ascorbic acid is special because it can transfer a single electron, owing to the resonance-stabilized nature of its own [[radical ion]], called [[dehydroascorbate|semidehydroascorbate]]. The net reaction is:

:RO<sup>•</sup> + {{chem|C|6|H|7|O|6|−}} → RO<sup>−</sup> + C<sub>6</sub>H<sub>7</sub>O{{su|b=6|p=•}} → ROH + C<sub>6</sub>H<sub>6</sub>O<sub>6</sub><ref>{{citation | website = MetaCyc | url = http://www.biocyc.org/META/NEW-IMAGE?type=COMPOUND&object=CPD-318 | title = MetaCyc Compound: monodehydroascorbate radical | date = Aug 19, 2009 | vauthors = Caspi R | access-date=2014-12-08}}</ref>

On exposure to [[oxygen]], ascorbic acid will undergo further oxidative decomposition to various products including [[diketogulonic acid]], [[xylonic acid]], [[threonic acid]] and [[oxalic acid]].<ref>{{Cite book | url=https://books.google.com/?id=AJW37Xc3uiAC&pg=PA311&dq=decomposition+of+ascorbic+acid |title = Ingredient Interactions: Effects on Food Quality, Second Edition|isbn = 9781420028133|last1 = Gaonkar|first1 = Anilkumar G.|last2 = McPherson|first2 = Andrew | name-list-format = vanc |date = 2016-04-19}}</ref>

Reactive oxygen species are damaging to animals and plants at the molecular level due to their possible interaction with [[nucleic acid]]s, proteins, and lipids. Sometimes these radicals initiate chain reactions. Ascorbate can terminate these chain radical reactions by [[electron transfer]].  The oxidized forms of ascorbate are relatively unreactive and do not cause cellular damage.

However, being a good electron donor, excess ascorbate in the presence of free metal ions can not only promote but also initiate free radical reactions, thus making it a potentially dangerous pro-oxidative compound in certain metabolic contexts.

Ascorbic acid and its sodium, potassium, and calcium [[Salt (chemistry)|salt]]s are commonly used as [[antioxidant]] [[food additive]]s. These compounds are water-soluble and, thus, cannot protect [[fat]]s from oxidation: For this purpose, the fat-[[Solubility|soluble]] [[ester]]s of ascorbic acid with long-chain [[fatty acid]]s (ascorbyl palmitate or ascorbyl stearate) can be used as food antioxidants.

===Other reactions===
It creates volatile compounds when mixed with [[glucose]] and [[amino acid]]s in 90&nbsp;°C.<ref>{{cite journal |author1=Seck, S. |author2=Crouzet, J. | title = Formation of Volatile Compounds in Sugar-Phenylalanine and Ascorbic Acid-Phenylalanine Model Systems during Heat Treatment | journal = Journal of Food Science | year = 1981 | volume = 46 | issue = 3 | pages = 790–793 | doi = 10.1111/j.1365-2621.1981.tb15349.x }}</ref>

It is a cofactor in [[tyrosine]] [[oxidation]].<ref>{{cite journal | vauthors = Sealock RR, Goodland RL, Sumerwell WN, Brierly JM | title = The role of ascorbic acid in the oxidation of <small>L</small>-Tyrosine by guinea pig liver extracts | journal = The Journal of Biological Chemistry | volume = 196 | issue = 2 | pages = 761–7 | date = May 1952 | pmid = 12981016 | url = http://www.jbc.org/content/196/2/761.full.pdf }}</ref>

==Uses==
===Food additive===
The main use of {{sm|l}}-ascorbic acid and its salts is as food additives, mostly to combat oxidation.  It is approved for this purpose in the EU with [[E number]] E300,<ref name="food.gov.uk">UK Food Standards Agency: {{cite web |url=http://www.food.gov.uk/safereating/chemsafe/additivesbranch/enumberlist |title=Current EU approved additives and their E Numbers |access-date=2011-10-27}}</ref> USA,<ref name="fda.gov">US Food and Drug Administration: {{cite web|url=https://www.fda.gov/Food/FoodIngredientsPackaging/FoodAdditives/FoodAdditiveListings/ucm091048.htm |title=Listing of Food Additives Status Part I |access-date=2011-10-27 |url-status = dead|archive-url=https://web.archive.org/web/20120117060614/https://www.fda.gov/Food/FoodIngredientsPackaging/FoodAdditives/FoodAdditiveListings/ucm091048.htm |archive-date=2012-01-17 |df= }}</ref> Australia, and New Zealand)<ref name="comlaw.gov.au">Australia New Zealand Food Standards Code{{cite web |url=http://www.comlaw.gov.au/Details/F2011C00827 |title=Standard 1.2.4 – Labelling of ingredients |access-date=2011-10-27}}</ref>

===Dietary supplement===
Another major use of {{sm|l}}-ascorbic acid is as [[dietary supplement]].

===Niche, non-food uses===

* Ascorbic acid is easily oxidized and so is used as a reductant in photographic developer solutions (among others) and as a [[preservative]].
* In [[fluorescence microscope|fluorescence microscopy]] and related fluorescence-based techniques, ascorbic acid can be used as an [[antioxidant]] to increase fluorescent signal and chemically retard dye [[photobleaching]].<ref>{{cite journal | vauthors = Widengren J, Chmyrov A, Eggeling C, Löfdahl PA, Seidel CA | title = Strategies to improve photostabilities in ultrasensitive fluorescence spectroscopy | journal = The Journal of Physical Chemistry A | volume = 111 | issue = 3 | pages = 429–40 | date = January 2007 | pmid = 17228891 | doi = 10.1021/jp0646325 | bibcode = 2007JPCA..111..429W }}</ref>
* It is also commonly used to remove dissolved metal stains, such as iron, from fiberglass swimming pool surfaces.
* In plastic manufacturing, ascorbic acid can be used to assemble molecular chains more quickly and with less waste than traditional synthesis methods.<ref>{{citation |title=Vitamin C, water have benefits for plastic manufacturing |url=http://reliableplant.com/article.asp?pagetitle=Vitamin%20C,%20water%20have%20benefits%20for%20plastic%20manufacturing&articleid=3133 |publisher=Reliable Plant Magazine |year=2007 |access-date=2007-06-25 |archive-url=https://web.archive.org/web/20070927230356/http://www.reliableplant.com/article.asp?pagetitle=Vitamin+C%2C+water+have+benefits+for+plastic+manufacturing&articleid=3133 |archive-date=2007-09-27 |url-status = dead|df= }}</ref>
* Heroin users are known to use ascorbic acid as a means to convert heroin base to a water-soluble salt so that it can be injected.<ref>{{cite journal | vauthors = Beynon CM, McVeigh J, Chandler M, Wareing M, Bellis MA | title = The impact of citrate introduction at UK syringe exchange programmes: a retrospective cohort study in Cheshire and Merseyside, UK | journal = Harm Reduction Journal | volume = 4 | issue = 1 | pages = 21 | date = December 2007 | pmid = 18072971 | pmc = 2245922 | doi = 10.1186/1477-7517-4-21 }}</ref>
* As justified by its reaction with iodine, it is used to negate the effects of iodine tablets in water purification. It reacts with the sterilized water, removing the taste, color, and smell of the iodine. This is why it is often sold as a second set of tablets in most sporting goods stores as Potable Aqua-Neutralizing Tablets, along with the potassium iodide tablets.
*[[Intravenous therapy|Intravenous]] high-dose ascorbate is being used as a [[Chemotherapy|chemotherapeutic]] and [[Biological response modifiers|biological response modifying agent]].<ref>{{cite journal |title=The Riordan IVC Protocol for Adjunctive Cancer Care: Intravenous Ascorbate as a Chemotherapeutic and Biological Response Modifying Agent|url=http://www.doctoryourself.com/RiordanIVC.pdf|publisher=Riordan Clinic Research Institut|access-date=2 February 2014|date=February 2013}}</ref> Currently it is still under clinical trials.<ref>{{cite web |title=High-Dose Vitamin C (PDQ®): Human/Clinical Studies|url=http://www.cancer.gov/cancertopics/pdq/cam/highdosevitaminc/healthprofessional/page5|publisher=National Cancer Institute|access-date=2 February 2014|date=2013-02-08}}</ref>

==Synthesis==
Natural [[vitamin C|biosynthesis of vitamin C]] occurs in many plants, and animals, by a variety of processes.

===Industrial preparation===
[[Image:Synthesis ascorbic acid.svg|thumb|500px|The outdated, but historically important industrial synthesis of ascorbic acid from glucose via the [[Reichstein process]].]]
Eighty percent of the world's supply of ascorbic acid is produced in China.<ref>{{citation | newspaper = Washington Post | url = https://www.washingtonpost.com/wp-dyn/content/article/2007/05/19/AR2007051901273.html | title = Tainted Chinese Imports Common | date = May 20, 2007 | first=Rick | last=Weiss | name-list-format = vanc | access-date=2010-04-25}}</ref>
Ascorbic acid is prepared in industry from [[glucose]] in a method based on the historical [[Reichstein process]].  In the first of a five-step process, glucose is catalytically [[hydrogenation|hydrogenated]] to [[sorbitol]], which is then [[redox|oxidized]] by the [[microorganism]] ''[[Acetic acid bacteria#Acetobacter|Acetobacter]] suboxydans'' to [[sorbose]]. Only one of the six hydroxy groups is oxidized by this enzymatic reaction.  From this point, two routes are available.  Treatment of the product with [[acetone]] in the presence of an acid [[Catalysis|catalyst]] converts four of the remaining [[hydroxyl]] groups to [[acetal]]s. The unprotected hydroxyl group is oxidized to the carboxylic acid by reaction with the catalytic oxidant [[TEMPO]] (regenerated by [[sodium hypochlorite]] — [[bleach]]ing solution). Historically, industrial preparation via the Reichstein process used [[potassium permanganate]] as the bleaching solution.  Acid-catalyzed hydrolysis of this product performs the dual function of removing the two acetal groups and [[lactone|ring-closing lactonization]]. This step yields ascorbic acid. Each of the five steps has a yield larger than 90%.<ref>{{Ullmann | author = Eggersdorfer, M. |display-authors=etal| title = Vitamins | doi = 10.1002/14356007.a27_443 }}</ref>

A more biotechnological process, first developed in China in the 1960s, but further developed in the 1990s,  bypasses the use of acetone-protecting groups. A second [[genetically modified]] microbe species, such as mutant ''[[Erwinia]]'', among others, oxidises sorbose into [[2-ketogluconic acid]] (2-KGA), which can then undergo ring-closing lactonization via dehydration. This method is used in the predominant process used by the ascorbic acid industry in China, which supplies 80% of world's ascorbic acid.<ref>[http://www.csmonitor.com/2007/0720/p01s01-woap.html China's grip on key food additive / The Christian Science Monitor]. CSMonitor.com (2007-07-20). Retrieved on 2012-12-04.</ref> American and Chinese researchers are competing to engineer a mutant that can carry out a [[one-pot synthesis|one-pot fermentation]] directly from glucose to 2-KGA, bypassing both the need for a second fermentation and the need to reduce glucose to sorbitol.<ref>[http://www.competition-commission.org.uk/rep_pub/reports/2001/fulltext/456a5.1.pdf BASF’s description of vitamin C—developments in production methods] {{webarchive |url=https://web.archive.org/web/20120130183916/http://www.competition-commission.org.uk/rep_pub/reports/2001/fulltext/456a5.1.pdf |date=January 30, 2012 }}. competition-commission.org.uk</ref>

There exists a {{sm|d}}-ascorbic acid, which does not occur in nature but can be synthesized artificially. To be specific, {{sm|l}}-ascorbate is known to participate in many specific enzyme reactions that require the correct enantiomer ({{sm|l}}-ascorbate and not {{sm|d}}-ascorbate).<ref>{{Cite journal|last=Rosa|first=Júlio César Câmara|last2=Colombo|first2=Lívia Tavares|last3=Alvim|first3=Mariana Caroline Tocantins|last4=Avonce|first4=Nelson|last5=Van Dijck|first5=Patrick|last6=Passos|first6=Flávia Maria Lopes|date=2013-06-22|title=Metabolic engineering of Kluyveromyces lactis for L-ascorbic acid (vitamin C) biosynthesis|journal=Microbial Cell Factories|volume=12|pages=59|doi=10.1186/1475-2859-12-59|issn=1475-2859|pmc=3699391|pmid=23799937}}</ref>  {{sm|l}}-Ascorbic acid has a [[specific rotation]] of [α]{{su|b=D|p=20}}&nbsp;=&nbsp;+23°.<ref>{{cite book |last=Davies|first=Michael B. | name-list-format = vanc |title=Vitamin C : its chemistry and biochemistry|date=1991|publisher=Royal Society of Chemistry|location=Cambridge [Cambridgeshire]|isbn=9780851863337|author2=Austin, John A. |author3=Partridge, David A. |url= https://books.google.com/?id=gMe5LCZLm2kC&pg=PA35&dq=%22ascorbate%22+specific+rotation }}</ref>

===Determination===
The traditional way to analyze the ascorbic acid content is the process of [[titration]] with an [[oxidizing agent]], and several procedures have been developed.

The popular [[iodometry]] approach uses [[iodine]] in the presence of a [[starch indicator]]. Iodine is reduced by ascorbic acid, and, when all the ascorbic acid has reacted, the iodine is then in excess, forming a blue-black complex with the starch indicator.  This indicates the end-point of the titration.

As an alternative, ascorbic acid can be treated with iodine in excess, followed by back titration with sodium thiosulfate using starch as an indicator.<ref>{{cite journal|url=http://www.saps.org.uk/attachments/article/556/simple_test_for_vitamin_c.pdf |title=A Simple Test for Vitamin C |journal=School Science Review |year=2002 |volume=83 |issue=305 |page=131 |archive-url=https://web.archive.org/web/20160704170133/http://www.saps.org.uk/attachments/article/556/simple_test_for_vitamin_c.pdf |archive-date=July 4, 2016}}</ref>

This iodometric method has been revised to exploit reaction of ascorbic acid with [[iodate]] and [[iodide]] in [[acid]] solution. Electrolyzing the solution of potassium iodide produces iodine, which reacts with ascorbic acid. The end of process is determined by [[potentiometric titration]] in a manner similar to [[Karl Fischer titration]]. The amount of ascorbic acid can be calculated by [[Faraday's laws of electrolysis|Faraday's law]].

Another alternative uses [[N-Bromosuccinimide|''N''-bromosuccinimide]] (NBS) as the oxidizing agent, in the presence of [[potassium iodide]] and starch. The NBS first oxidizes the ascorbic acid; when the latter is exhausted, the NBS liberates the iodine from the potassium iodide, which then forms the blue-black complex with starch.

== See also ==
* [[Colour retention agent]]
* [[Erythorbic acid]]: a [[diastereomer]] of ascorbic acid.
* [[Mineral ascorbates]]: salts of ascorbic acid
* [[Acids in wine]]

==Notes and references==
{{Reflist|30em}}

== Further reading ==
{{refbegin}}
* {{cite book | vauthors = Clayden J, Greeves N, Warren S, Wothers P | title = Organic Chemistry | publisher = Oxford University Press | year = 2001 | isbn = 0-19-850346-6 | url-access = registration | url = https://archive.org/details/organicchemistry00clay_0 }}
* {{cite book | title = Vitamin C: Its Chemistry and Biochemistry | first1 = Michael B. | last1 = Davies | first2 = John | last2 = Austin | first3 = David A. | last3 = Partridge | name-list-format = vanc | publisher = Royal Society of Chemistry | isbn = 0-85186-333-7| year = 1991 }}
* {{cite book | title = Food: The Chemistry of Its Components | edition = 3rd | first = T. P. | last = Coultate | year = 1996 | name-list-format = vanc | publisher = Royal Society of Chemistry | isbn = 0-85404-513-9 | url-access = registration | url = https://archive.org/details/foodchemistryofi0000coul }}
* {{cite book | editor1-last = Gruenwald | editor1-first = J. | editor2-last = Brendler | editor2-first = T. | editor3-last = Jaenicke | editor3-first = C. | name-list-format = vanc | title = PDR for Herbal Medicines | url = https://archive.org/details/pdrforherbalmedi00joer_0 | url-access = registration | edition = 3rd | publisher = Thomson PDR | location = Montvale, New Jersey | year = 2004}}
* {{cite book | first1 = John | last1 = McMurry | name-list-format = vanc | title = Organic Chemistry | publisher = Thomson Learning | year = 2008 | edition = 7e | isbn = 978-0-495-11628-8}}
{{refend}}

== External links ==
{{Commons category}}
*{{ICSC|0379|03}}
*{{SIDS|name=<small>L</small>-Ascorbic acid|id=50817}}
*[http://www.inchem.org/documents/pims/pharm/ascorbic.htm IPCS Poisons Information Monograph (PIM) 046]
*[http://www.bruker-axs.de/fileadmin/user_upload/SMART_X2S_Structure_Gallery/Structures/vitc_1006.html Interactive 3D-structure of vitamin C] with details on the x-ray structure

{{Gynecological anti-infectives and antiseptics}}
{{Vitamins}}
{{Enzyme cofactors}}
{{Antioxidants}}
{{Authority control}}

{{DEFAULTSORT:Ascorbic Acid}}
[[Category:Organic acids]]
[[Category:Antioxidants]]
[[Category:Dietary antioxidants]]
[[Category:Coenzymes]]
[[Category:Corrosion inhibitors]]
[[Category:Furanones]]
[[Category:Vitamers]]
[[Category:Vitamin C]]
[[Category:Biomolecules]]
[[Category:3-hydroxypropenals]]
        """
        f = Fragmenter()
        result = Compiler().compile(text)
        print(f.frag(result, ['nucleic', 'acid']))

if __name__ == '__main__':
    unittest.main()
