import axios from 'axios'

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
})

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      'Content-Type': 'application/json'
    }
    if (token != null) {
      headers.authorization = 'Bearer ' + token
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data
    })
      .then((response) => {
        return { status: response.status, data: response.data }
      })
      .catch((error) => {
        console.error(error)
      })
  },
  getQuizInfo() {
    return this.call('get', 'quiz-info')
  },
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },
  getPlayersData() {
    return this.call("get", 'players');
  },
  async setNewPlayer(player){
    return this.call("post", "participations", player);
  },
  async login(password) {
    return this.call("post", "login", password);
  },
  async deleteQuestion(id, token){
    return this.call("delete", `questions/${id}`, null, token);
  },
  async updateQuestion(id, data, token){
    return this.call("put", `questions/${id}`, data, token);
  },
  async addQuestion(data, token) {
    return this.call("post", "questions", data, token);
  }
}
