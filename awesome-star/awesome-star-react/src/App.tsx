import './App.css';
import {Bar} from 'react-chartjs-2';
import * as React from 'react';
import * as ReactMarkdown from 'react-markdown';
import axios from 'axios';
//const Spinner = require('react-spinkit')
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
  maxCounter: number,
  topRepos: GithubRepo[],
  chartData: any
}

class App extends React.Component<{}, MyState> {

  constructor(props: any) {
    super(props);
    this.state = {
      markdown: "# Empty",
      counter: 0,
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
    const url = 'https://github.com/vinta/awesome-python';
    let repos: GithubRepo[] = [];
    let chartdata: any = [];
    let counter = 0;
    let maxCounter = 0;

    const axiosConf = {
      headers: {
        // You need to replace XXXX to your token string for Github
        Authorization: 'token XXXX'
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
      repos.push(repoInfo);
    }
    maxCounter = repos.length;
    this.setState({maxCounter: maxCounter})

    repos[0].star = 1000;
    repos[1].star = 100;
    repos[2].star = 500;
    repos[3].star = 0;
    repos[4].star = 200;

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
    const topRepos = repos.slice(0, 5);
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
    this.setState({markdown: markdownData})
  }

  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>

        {/* Input Part */}
        <div>Markdown Entry</div>
        <hr/>
        <input type="button" value="GET" onClick={this.getGithub} />
        <div>Current: {this.state.counter}/{this.state.maxCounter}</div>

        {/* Top N repositories list Part */}
        {this.state.topRepos.map((elem, index) => {
          return <h3 key={index}>... No.{index+1} : {elem.repo} ({elem.star} stars)</h3>;
        })}


        {/* Chart Part */}
        <Bar data={this.state.chartData} />

        {/* Spinner Part */}
        {
          this.state.counter != this.state.maxCounter
            ? <Spinner name="ball-beat" />
            : <div></div>
        }

        {/* Markdown Part */}
        <ReactMarkdown 
          source={this.state.markdown}
          escapeHtml={false}
        />
      </div>
    );
  }
}

export default App;
