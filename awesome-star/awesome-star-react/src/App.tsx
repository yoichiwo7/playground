import * as React from 'react';
import * as ReactMarkdown from 'react-markdown';
import GithubInput from './component/GithubInput'
import GithubTopResult from './component/GithubTopResult'
import {GithubRepo} from './component/GithubInput'

import './App.css';
import logo from './logo.svg';

type MyState = {
  url: string,
  token: string,
  repos: GithubRepo[],
  topN: number,
  markdown: string,
}

class App extends React.Component<{}, MyState> {

  constructor(props: any) {
    super(props);
    this.state = {
      url: "https://github.com/akrawchyk/awesome-vim",
      token: "",
      repos: [],
      topN: 5,
      markdown: "**Awesome repository page with start will be displayed here**",
    };
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
          onCompleted={this.onCompleted}
        />

        <GithubTopResult
          repos={this.state.repos}
          topN={this.state.topN}
        />

        <ReactMarkdown
          source={this.state.markdown}
          escapeHtml={false}
          skipHtml={false}
        />
      </div>
    );
  }
}

export default App;
