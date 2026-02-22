import axios from 'axios';

// In dev, Vite proxies /api → localhost:8000 (see vite.config.js).
// In production (Vercel), VITE_API_URL must be set to the Railway backend URL.
const BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

const api = axios.create({ baseURL: BASE });


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
