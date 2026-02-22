import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

export async function fetchScenarios() {
  const { data } = await api.get('/scenarios');
  return data.scenarios;
}

export async function fetchPathways() {
  const { data } = await api.get('/pathways');
  return data.pathways;
}

export async function runSimulation(params) {
  const { data } = await api.post('/simulate', params);
  return data;
}

export async function fetchQuiz(pathway) {
  const { data } = await api.get(`/quiz/${pathway}`);
  return data;
}

export async function checkAnswer(pathway, questionId, answerIndex) {
  const { data } = await api.post(`/quiz/${pathway}/check`, {
    question_id: questionId,
    answer_index: answerIndex,
  });
  return data;
}
