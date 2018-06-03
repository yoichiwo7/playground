<template>
  <div class="home">
    <div>
      <input title="Enter the awesome repo URL" v-model="url" type="text" name="abcde" id="awesome-repo">
    </div>
    <button @click="getGithub">GET</button>

    <div>Retrived: <b>{{currentCounter}}</b></div>

    <div>Chart: <bar-chart :data="chartdata"></bar-chart></div>

    <div>Elements of axios response status</div>
    <!-- <pre>{{markdown}}</pre> -->
    <vue-markdown :source="markdown"></vue-markdown>

    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
//import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import axios from 'axios';
import VueMarkdown from 'vue-markdown';
import 'chart.js';
//@ts-ignore
import VueChartkick from 'vue-chartkick';

class GithubRepo {
  description = "";
  url = "";
  user = "";
  repo = "";
  star = 0;
}

Vue.use(VueChartkick);

@Component({
  components: {
    VueMarkdown,
  },
})
export default class Home extends Vue {

  private url = 'https://github.com/vinta/awesome-python';
  private markdown = `EMPTY`;
  private repos: GithubRepo[] = [];
  private counter = 0;
  private chartdata: any = [];
  private maxCounter = 0;
  private flag = true;

  get currentCounter() {
    return `${this.counter} / ${this.maxCounter}`
  }

  private async getGithub() {
    const axiosConf = {
      headers: {
        // You need to replace XXXX to your token string for Github
        Authorization: 'token XXXX'
      }
    }
    const urlPattern = /^https:\/\/github.com\/(.+?)\/(.+?)\/?$/;
    const match = this.url.match(urlPattern);
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
      this.repos.push(repoInfo);
    }
    this.maxCounter = this.repos.length;

    this.repos[0].star = 1000;
    this.repos[1].star = 100;
    this.repos[2].star = 500;
    this.repos[3].star = 0;
    this.repos[4].star = 200;

    this.chartdata = this.repos.map((e) => [e.repo, e.star]);
    this.chartdata.length = 5;


    // const jobs: any[] = [];
    // this.repos.forEach((entry) => {
    //   const job = axios.get(`https://api.github.com/repos/${entry.user}/${entry.repo}`, axiosConf)
    //   .then((res) => {
    //     entry.star = res.data.stargazers_count;
    //     console.log(`${entry.description}, ${entry.user}, ${entry.repo}, **${entry.star}**`);
    //     this.counter++;
    //   })
    //   .catch((r) => {
    //     console.log(r);
    //   });
    //   jobs.push(job);
    // });
    // // wait all
    // await axios.all(jobs);

    let markdownData: string = resReadme.data;
    this.repos.forEach((entry) => {
      markdownData = markdownData.replace(
        `[${entry.description}]`,
        `[${entry.description} <font color="Red">:star:${entry.star}</font>]`);
    });
    this.markdown = markdownData;
  }
}
</script>
