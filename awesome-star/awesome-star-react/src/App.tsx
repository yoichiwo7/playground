import './App.css';
import { Bar } from 'react-chartjs-2';
import * as React from 'react';
import * as ReactMarkdown from 'react-markdown';
import * as Spinner from 'react-spinkit'
import GithubInput from './component/GithubInput'
import {GithubRepo} from './component/GithubInput'

import logo from './logo.svg';
import { url } from 'inspector';

type MyState = {
  url: string,
  token: string,
  counter: number,
  maxCounter: number,
  repos: GithubRepo[],
  topN: number,
  markdown: string,
}

class App extends React.Component<{}, MyState> {

  chartOptions = {
    scales: {
      yAxes: [{ ticks: { beginAtZero: true } }]
    }
  }

  constructor(props: any) {
    super(props);
    this.state = {
      url: "https://github.com/akrawchyk/awesome-vim",
      token: "",
      counter: 0,
      maxCounter: 0,
      repos: [],
      topN: 5,
      markdown: "**Awesome repository page with start will be displayed here**",
    };
  }

  onUpdated = (current: number, max: number) => {
    this.setState({
      counter: current,
      maxCounter: max
    })
  }

  onCompleted = (awesomeReadme: string, updatedRepos: GithubRepo[], topN: number) => {
    const staredMarkdown = this.getStaredMarkdown(awesomeReadme, updatedRepos);
    this.setState({
      topN: topN,
      repos: updatedRepos,
      markdown: staredMarkdown
    })
  }

  onUrlChange = (e: any) => {
    this.setState({
      url: e.target.value
    })
  }

  onTokenChange = (e: any) => {
    this.setState({
      token: e.target.value
    })
  }

  onTopnChange = (e: any) => {
    this.setState({
      topN: Number(e.target.value)
    })
  }

  getStaredMarkdown = (readme: string, repos: GithubRepo[]) => {
    let markdownData: string = readme;
    repos.forEach((entry) => {
      const starStr = "★".repeat(Math.min((entry.star / 1000) + 1, 5))
      // TODO: make the string manipulation more efficient
      markdownData = markdownData.replace(
        `[${entry.description}]`,
        `[${entry.description}  **${starStr}${entry.star}**]`);
    });
    return markdownData;
  }

  getChartData = () => {
    const topRepos = this.state.repos.slice(0, this.state.topN)
    return {
      labels: topRepos.map((e) => e.repo),
      datasets: [
        {
          data: topRepos.map((e) => e.star),
          label: "Star",
          borderWidth: 4,
          borderColor: 'rgba(132, 99, 255, 1.0)',
          backgroundColor: 'rgba(132, 99, 255, 0.4)',
        }
      ],
    }
  }

  public render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Awesome Star [ version=0.0.1 ]</h1>
        </header>

        <GithubInput 
          url={this.state.url}
          token={this.state.token}
          topRepoNum={this.state.topN}
          showHelp={true}
          onUrlChange={this.onUrlChange}
          onTokenChange={this.onTokenChange}
          onTopnChange={this.onTopnChange}
          onUpdated={this.onUpdated}
          onCompleted={this.onCompleted}
        />


        { this.state.maxCounter > 0
          && <div>[Current/Max] :  {this.state.counter}/{this.state.maxCounter}</div>}
        {/* Spinner Part */}
        {this.state.counter != this.state.maxCounter
          ? <Spinner name="ball-beat" />
          : <div></div>
        }

        {/* Top N repositories list Part */}
        {this.state.repos.length > 0 
          && <h2>Top {this.state.topN} List</h2>}
        {this.state.repos.slice(0, this.state.topN).map((elem, index) => 
            <h5 key={index}>... No.{index + 1} : {elem.repo} ({elem.star} stars)</h5>
        )}

        {/* Chart Part */}
        {this.state.repos.length > 0
          && <h2>Top {this.state.topN} Chart</h2>}
        {this.state.repos.length > 0
          && <Bar data={this.getChartData()} options={this.chartOptions} />
        }

        <ReactMarkdown
          source={this.state.markdown} escapeHtml={false} skipHtml={false}
        />
      </div>
    );
  }
}

export default App;
