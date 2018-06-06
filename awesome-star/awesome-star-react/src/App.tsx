import './App.css';
import {Bar} from 'react-chartjs-2';
import * as React from 'react';
import * as ReactMarkdown from 'react-markdown';
import axios from 'axios';
import * as Spinner from 'react-spinkit'


import logo from './logo.svg';

class GithubRepo {
  description = "";
  url = "";
  user = "";
  repo = "";
  star = 0;
}

type MyState = {
  markdown: string,
  counter: number,
  url: string,
  token: string,
  topN: number,
  completed: boolean,
  maxCounter: number,
  topRepos: GithubRepo[],
  chartData: any
}

class App extends React.Component<{}, MyState> {

  constructor(props: any) {
    super(props);
    this.state = {
      markdown: "**Awesome repository page with start will be displayed here**",
      counter: 0,
      url: 'https://github.com/vinta/awesome-python',
      token: '',
      topN: 10,
      completed: false,
      maxCounter: 0,
      topRepos: [],
      chartData: {
        datasets: [
          {
            data: [1, 2, 3, 6, 2],
            label: "Star",
          }
        ],
        labels: ['a', 'b', 'c', 'd', 'e'],
      }
    };
  }

  getGithub = async () => {
    const url = this.state.url
    let repos: GithubRepo[] = [];
    let repoKeys = new Set();
    let chartdata: any = [];
    let counter = 0;
    let maxCounter = 0;

    const axiosConf = {
      headers: {
        // You need to replace XXXX to your token string for Github
        Authorization: `token ${this.state.token}`
      }
    }
    const urlPattern = /^https:\/\/github.com\/(.+?)\/(.+?)\/?$/;
    const match = url.match(urlPattern);
    if (match == null) {
      return;
    }
    const user = match[1];
    const repo = match[2];
    const res = await axios.get(`https://api.github.com/repos/${user}/${repo}/readme`, axiosConf);
    const resReadme = await axios.get(res.data.download_url);

    const mdLinkPattern = /\[(.*?)\]\s*\((.*?)\)/g;
    let i = 0;
    while (true) {
      i++;
      let mdMatch = mdLinkPattern.exec(resReadme.data);
      if (mdMatch === null || mdMatch.length === 0) {
        // No more URL found
        break;
      }
      const [desc, url] = [mdMatch[1], mdMatch[2]];
      let urlMatch = url.match(urlPattern);
      if (urlMatch == null) {
        // Not Github repository URL
        continue;
      }
      const starUser = urlMatch[1];
      const starRepo = urlMatch[2].replace(/\/.*$/, '');
      const repoInfo = new GithubRepo();
      repoInfo.description = desc;
      repoInfo.user = starUser;
      repoInfo.repo = starRepo;
      repoInfo.url = urlMatch[0];
      if (!repoKeys.has(`${starUser}/${starRepo}`)) {
        repos.push(repoInfo);
      }
      repoKeys.add(`${starUser}/${starRepo}`)
    }
    maxCounter = repos.length;
    this.setState({maxCounter: maxCounter})

    chartdata = repos.map((e) => [e.repo, e.star]);
    chartdata.length = 5;


    const jobs: any[] = [];
    repos.forEach((entry) => {
      const job = axios.get(`https://api.github.com/repos/${entry.user}/${entry.repo}`, axiosConf)
      .then((res) => {
        entry.star = res.data.stargazers_count;
        console.log(`${entry.description}, ${entry.user}, ${entry.repo}, **${entry.star}**`);
        counter++;
        this.setState({ counter: counter })
      })
      .catch((r) => {
        console.log(r);
        counter++;
        this.setState({ counter: counter })
      });
      jobs.push(job);
    });
    // wait all
    await axios.all(jobs);

    repos.sort((a,b) => {
      if (a.star > b.star) {
        return -1;
      }
      if (a.star < b.star) {
        return 1;
      }
      return 0;
    })

    const topRepos = repos.slice(0, this.state.topN);
    this.setState({
      topRepos: topRepos,
      chartData: {
        datasets: [
          {
            data: topRepos.map((e) => e.star),
            label: "Star",
          }
        ],
        labels: topRepos.map((e) => e.repo)
      }
    });

    let markdownData: string = resReadme.data;
    repos.forEach((entry) => {
      markdownData = markdownData.replace(
        `[${entry.description}]`,
        `[${entry.description} **:-:-:${entry.star}:-:-:**]`);
    });
    this.setState({
      markdown: markdownData,
      completed: true
    })
  }

  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Awesome Star (for Github awesome repos)</h1>
        </header>

        {/* Input Part */}
        <div>Please Enter Github awesome repo URL and Github token</div>
        <div> URL: 
          <input type="text" value={this.state.url} size={80} name="url" id=""
          onChange={((e) => { this.setState({url: e.target.value}); })} />
        </div>
        <div> Token: 
          <input type="text" value={this.state.token} size={80} name="url" id=""
          onChange={((e) => { this.setState({token: e.target.value}); })} />
        </div>
        <div> Top List number: 
          <input type="text" value={this.state.topN} name="topn" id=""
          onChange={((e) => { this.setState({topN: Number(e.target.value)}); })} />
        </div>
        <input type="button" value="GET" onClick={this.getGithub} />
        <div>Retrieved Repos: {this.state.counter}/{this.state.maxCounter}</div>


        {/* Spinner Part */}
        {
          this.state.counter != this.state.maxCounter
            ? <Spinner name="ball-beat" />
            : <div>Not yet...</div>
        }

        {/* Top N repositories list Part */}
        <h2>Top {this.state.topN} List</h2>
        {this.state.topRepos.map((elem, index) => {
          return <h5 key={index}>... No.{index+1} : {elem.repo} ({elem.star} stars)</h5>;
        })}

        {/* Chart Part */}
        <h2>Top 5 Bar Chart</h2>
        {
          this.state.completed
            ? <Bar data={this.state.chartData} />
            : <div>Not yet...</div>
        }

        {/* Markdown Part */}
        <hr/>
        <ReactMarkdown 
          source={this.state.markdown}
          escapeHtml={false}
        />
      </div>
    );
  }
}

export default App;
