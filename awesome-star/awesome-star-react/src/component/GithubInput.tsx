import * as React from "react";
import axios from 'axios';
import * as http from 'http';
import * as https from 'https';
import * as Spinner from 'react-spinkit'

class GithubRepo {
  description = "";
  url = "";
  user = "";
  repo = "";
  star = -1;
  lastUpdated = "";
  license = "";
}

interface Props {
    url: string;
    token: string;
    topRepoNum: number,
    showHelp: boolean,
    onCompleted: any,
    onUrlChange: any,
    onTokenChange: any,
    onTopnChange: any,
}

type MyState = {
  counter: number,
  maxCounter: number
}

class GithubInput extends React.Component<Props, MyState> {
  GITHUB_URL_PATTERN = /^https:\/\/github.com\/(.+?)\/(.+?)\/?$/;
  MARKDOWN_LINK_PATTERN = /\[(.*?)\]\s*\((.*?)\)/g;

  constructor(props: Props) {
    super(props);

    this.state = {
      counter: 0,
      maxCounter: 0
    }
  }

  getGithub = async () => {
    const url = this.props.url;
    const awesomeReadme = await this.getReadme(url);
    const targetRepos = await this.getTargetRepos(awesomeReadme);
    await this.updateStarsByApi(targetRepos);
    this.props.onCompleted(awesomeReadme, targetRepos, this.props.topRepoNum);
  }

  getAxiosConf = () => {
    //NOTE: Avoid infinite connection by setting maxSockets of http(s).Agent
    let axiosConf: object = {
        httpAgent: new http.Agent({ keepAlive: true, maxSockets: 10 }),
        httpsAgent: new https.Agent({ keepAlive: true, maxSockets: 10 })
    };

    if (this.props.token.length !== 0) {
      axiosConf["headers"] = { Authorization: `token ${this.props.token}` };
    }
    return axiosConf;
  }

  getReadme = async (url: string) => {
    const match = url.match(this.GITHUB_URL_PATTERN);
    if (match == null) {
      return;
    }
    const user = match[1];
    const repo = match[2];
    const res = await axios.get(`https://api.github.com/repos/${user}/${repo}/readme`, this.getAxiosConf());
    const resReadme = await axios.get(res.data.download_url);
    return resReadme.data;
  }

  getTargetRepos = async (readme: string) => {
    const repos: GithubRepo[] = []
    const repoSet = new Set()

    let i = 0;
    while (true) {
      i++;
      let mdMatch = this.MARKDOWN_LINK_PATTERN.exec(readme);
      if (mdMatch === null || mdMatch.length === 0) {
        // No more URL found
        break;
      }
      const [desc, url] = [mdMatch[1], mdMatch[2]];
      let urlMatch = url.match(this.GITHUB_URL_PATTERN);
      if (urlMatch == null) {
        // Not Github repository URL
        continue;
      }
      const starUser = urlMatch[1];
      const starRepo = urlMatch[2].replace(/\/.*$/, '');

      const repoInfo = new GithubRepo();
      repoInfo.url = urlMatch[0];
      repoInfo.description = desc;
      repoInfo.user = starUser;
      repoInfo.repo = starRepo;
      if (!repoSet.has(`${starUser}/${starRepo}`)) {
        repos.push(repoInfo);
      }
      repoSet.add(`${starUser}/${starRepo}`);
    }
    this.setState({
      counter: 0,
      maxCounter: repos.length
    });
    return repos;
  }

  updateStarsByApi = async (repos: GithubRepo[]) => {
    let counter = 0;
    const jobs: any[] = [];
    repos.forEach((entry) => {
      const job = axios.get(`https://api.github.com/repos/${entry.user}/${entry.repo}`, this.getAxiosConf())
        .then((res) => {
          entry.star = res.data.stargazers_count;
          entry.lastUpdated = res.data.updated_at;
          entry.license = res.data.license.key;
          console.log(`${entry.description}, ${entry.user}, ${entry.repo}, **${entry.star}**`);
          this.setState({counter: ++counter});
        })
        .catch((r) => {
          console.log(r);
          this.setState({counter: ++counter});
        });
      jobs.push(job);
    });
    await axios.all(jobs);

    repos.sort((a, b) => {
      if (a.star > b.star) { return -1; }
      if (a.star < b.star) { return 1; }
      return 0;
    })
  }

  helpPane = () => {
    return (
      <div>
          <b>Awesome star</b> shows number of star in Github awesome repository.
          <ul>
              <li>Enter URL of Github awesome repository.</li>
              <li>Enter Github token. Need the token if hundreds of Github API calls are required.</li>
              <li>Without token Github API can be called only 60 calls per hour.</li>
              <li>With token Github API can be called 5000 calls per hour.</li>
          </ul>
      </div>
    );
  }

  render() {
    return (
      <div>
        { this.props.showHelp && this.helpPane()}

        <div>
          URL:
          <input type="text" size={80} name="url" id=""
            value={this.props.url} onChange={e => {this.props.onUrlChange(e)}}
          />
        </div>
        <div>
          Token:
          <input type="text" size={80} name="url" id=""
            value={this.props.token} onChange={e => {this.props.onTokenChange(e)}}
          />
        </div>
        <div>
          Top List number:
          <input
            type="text" name="topn" id=""
            value={this.props.topRepoNum} onChange={e => {this.props.onTopnChange(e)}}
          />
        </div>
        <input type="button" value="GET" onClick={this.getGithub} />

        { this.state.maxCounter > 0
          && <div>[Current/Max] :  {this.state.counter}/{this.state.maxCounter}</div>}
        {/* Spinner Part */}
        {this.state.counter != this.state.maxCounter
          ? <Spinner name="ball-beat" />
          : <div></div>
        }

      </div>
    );
  }
}

export default GithubInput;
export {GithubRepo};
