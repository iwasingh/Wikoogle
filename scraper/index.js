const fs = require("fs");
const sh = require("shelljs");
const puppeteer = require("puppeteer");

const keywords = [
    "DNA",
    "Apple",
    "Epigenetics",
    "Hollywood",
    "Maya",
    "Microsoft",
    "Precision",
    "Tuscany",
    "99 balloons",
    "Computer Programming",
    "Financial meltdown",
    "Justin Timberlake",
    "Least Squares",
    "Mars robots",
    "Page six",
    "Roman Empire",
    "Solar energy",
    "Statistical Significance",
    "Steve Jobs",
    "The Maya",
    "Triple Cross",
    "US Constitution",
    "Eye of Horus",
    "Madam I’m Adam",
    "Mean Average Precision",
    "Physics Nobel Prizes",
    "Read the manual",
    "Spanish Civil War",
    "Do geese see god",
    "Much ado about nothing"
]

async function evaluateGoogle(page, scrapeUrl, pageCount) {
    if (pageCount > 0) {
        scrapeUrl = scrapeUrl + "&start=" + pageCount * 10
    }

    await page.goto(scrapeUrl, {waitUntil: "load"});

    return page.evaluate(() => {
        let nodesAccumulator = []

        document
            .querySelectorAll("#rso div > div > div.r > a > h3")
            .forEach(node =>
                nodesAccumulator.push(
                    node.textContent
                        .replace(" - Wikipedia", "")
                        .replace("'", "")
                )
            )
        
        return nodesAccumulator
    });
}

async function evaluateWiki(page, scrapeUrl) {
    await page.goto(scrapeUrl, {waitUntil: "load"});

    return page.evaluate(() => {
        let nodesAccumulator = []

        document
            .querySelectorAll("body > div.page > main > article > a > h3")
            .forEach(node =>
                nodesAccumulator.push(
                    node.textContent
                        .replace(/\n/g, "")
                        .replace(/\t/g, "")
                        .replace(/^\d+. /g, "")
                        .replace("'", "")
                )
            )

        return nodesAccumulator
    });
}

async function runKeyForGoogle(k, page) {
    try {
        const rawdata = fs.readFileSync(".cache/.google/" + keywords[k] + ".json")
        return JSON.parse(rawdata)
    } catch (e) {
        console.error("could_not_read_from_cache")
    }

    let matches = []
    let pageCount = 0
    let failCount = 0

    let scrapeUrl = "https://www.google.com/search?q=site:en.wikipedia.org+" + keywords[k]

    while (matches.length < 30 && failCount < 10) {
        console.warn("fetching = ", matches.length, failCount)

        const nodes = await evaluateGoogle(page, scrapeUrl, pageCount)

        for (n in nodes) {
            if (matches.filter(function (_m) { return _m == n }).length == 0) {
                const cmd = "grep '\\- " + nodes[n] + " indexed' preprocessing.log | wc -l"
                const res = sh.exec(cmd, {silent: true}).stdout

                if (parseInt(res) != 0) {
                    failCount = 0
                    matches.push(nodes[n])
                }
            }
        }

        pageCount += 1
        failCount += 1
    }

    fs.writeFileSync(".cache/.google/" + keywords[k] + ".json", JSON.stringify(matches))

    return matches
}

async function runKeyForWiki(k, page, ns) {
    let settingsUrl = "http://212.237.42.43:8080/settings"
    let scrapeUrl   = "http://212.237.42.43:8080/search?q=" + keywords[k]

    try {
        const rawdata = fs.readFileSync(".cache/." + ns + "/" + keywords[k] + ".json")
        return JSON.parse(rawdata)
    } catch (e) {
        console.error("could_not_read_from_cache")
    }

    await page.goto(settingsUrl, {waitUntil: "load"})

    const matches = await evaluateWiki(page, scrapeUrl)

    fs.writeFileSync(".cache/." + ns + "/" + keywords[k] + ".json", JSON.stringify(matches))

    return matches
}


const DEFAULT_SETTINGS = {
    "results_limit": "30",
    "query_expansion": "none",
    "link_analysis": "none"
}

const BM25 = {"ranking": "bm25"}
const PL2  = {"ranking": "pl2" }

const LCA       = {"query_expansion": "lca"      }
const THESAURUS = {"query_expansion": "thesaurus"}

const PAGE_RANK = {"link_analysis": "page_rank"}
const HITS_RANK = {"link_analysis": "hits_rank"}

const BM25_DEFAULT = {...DEFAULT_SETTINGS, ...BM25, "name": "bm25"}

const BM25_LCA       = {...BM25_DEFAULT, ...LCA,       "name": "bm25_lca"}
const BM25_THESAURUS = {...BM25_DEFAULT, ...THESAURUS, "name": "bm25_thesaurus"}

const BM25_PAGE_RANK = {...BM25_DEFAULT, ...PAGE_RANK, "name": "bm25_page_rank"}
const BM25_HITS_RANK = {...BM25_DEFAULT, ...HITS_RANK, "name": "bm25_hits_rank"}

const BM25_LCA_PAGE_RANK = {...BM25_LCA, ...PAGE_RANK, "name": "bm25_lca_page_rank"}
const BM25_LCA_HITS_RANK = {...BM25_LCA, ...HITS_RANK, "name": "bm25_lca_hits_rank"}

const BM25_THESAURUS_PAGE_RANK = {...BM25_THESAURUS, ...PAGE_RANK, "name": "bm25_thesaurus_page_rank"}
const BM25_THESAURUS_HITS_RANK = {...BM25_THESAURUS, ...HITS_RANK, "name": "bm25_thesaurus_hits_rank"}

const PL2_DEFAULT = {...DEFAULT_SETTINGS, ...PL2, "name": "pl2"}

const PL2_LCA       = {...PL2_DEFAULT, ...LCA,       "name": "pl2_lca"}
const PL2_THESAURUS = {...PL2_DEFAULT, ...THESAURUS, "name": "pl2_thesaurus"}

const PL2_PAGE_RANK = {...PL2_DEFAULT, ...PAGE_RANK, "name": "pl2_page_rank"}
const PL2_HITS_RANK = {...PL2_DEFAULT, ...HITS_RANK, "name": "pl2_hits_rank"}

const PL2_LCA_PAGE_RANK = {...PL2_LCA, ...PAGE_RANK, "name": "pl2_lca_page_rank"}
const PL2_LCA_HITS_RANK = {...PL2_LCA, ...HITS_RANK, "name": "pl2_lca_hits_rank"}

const PL2_THESAURUS_PAGE_RANK = {...PL2_THESAURUS, ...PAGE_RANK, "name": "pl2_thesaurus_page_rank"}
const PL2_THESAURUS_HITS_RANK = {...PL2_THESAURUS, ...HITS_RANK, "name": "pl2_thesaurus_hits_rank"}

const ALL_CONFIG = [
    BM25_DEFAULT,
    BM25_LCA,
    BM25_THESAURUS,
    BM25_PAGE_RANK,
    BM25_HITS_RANK,
    BM25_LCA_PAGE_RANK,
    BM25_LCA_HITS_RANK,
    BM25_THESAURUS_PAGE_RANK,
    BM25_THESAURUS_HITS_RANK,
    PL2_DEFAULT,
    PL2_LCA,
    PL2_THESAURUS,
    PL2_PAGE_RANK,
    PL2_HITS_RANK,
    PL2_LCA_PAGE_RANK,
    PL2_LCA_HITS_RANK,
    PL2_THESAURUS_PAGE_RANK,
    PL2_THESAURUS_HITS_RANK
]

let _configToApply = null

async function main() {
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox' /* fix kernel */
        ]
    });

    const page = await browser.newPage();

    await page.setRequestInterception(true)

    page.on("request", interceptedRequest => {
        if (_configToApply) {
            console.warn(_configToApply)

            interceptedRequest.continue({
                method: "POST",
                postData: _configToApply,
                headers: {
                    ...interceptedRequest.headers(),
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            _configToApply = null
        } else {
            interceptedRequest.continue()
        }
    });

    const _totals = []

    for (k in keywords) {
        _totals[k] = []

        const _google = await runKeyForGoogle(k, page)

        for (c in ALL_CONFIG) {
            _totals[k][c] = []

            const config = ALL_CONFIG[c]

            _configToApply = Object
                .entries(config)
                .concat([["kwarg", keywords[k]]])
                .map(function (e) {
                    return e[0] + "=" + e[1]
                })
                .join("&")
            
            const _tempda = await runKeyForWiki(k, page, config.name)
            const _wiki = _tempda.slice(0, 10)
            const _relv = _google.slice(0, 10)
            let _prec = [];

            for (p in _wiki) {
                if (_relv.includes(_wiki[p])) {
                    // console.warn(_wiki[p], parseInt(p) + 1)

                    const _v = (
                        (_prec.length + 1) /
                        (parseInt(p)  + 1) * 
                        100
                    )

                    _prec.push([_wiki[p], parseInt(_v)])
                }
            }

            for (r in _relv) {
                if (!_wiki.includes(_relv[r])) {
                    _prec.push([_relv[r], 0])
                }
            }

           _prec = [["-", 0], ..._prec]

            for (v in _prec) {
                for (t = parseInt(v); t <= 10; t++) {
                    if (_prec[t][1] > _prec[v][1]) {
                        _prec[v][1] = _prec[t][1]
                    }
                }
            }

            for (v in _prec) {
                _totals[k][c][v] = _prec[v][1]
            }
            // break // @
        }
        // break // @
    }

    for (c in ALL_CONFIG) {
        console.log('\n')
        console.log(keywords.join(","))

        for (i = 0; i <= 10; i++) {
            const _temp = []

            for (k in keywords) {
                _temp.push(_totals[k][c][i])
            }
            
            console.log(_temp.join(","))
        }
        // DNA[0], EPI[0], HOL[0]
    }

    await browser.close()
}

main()
