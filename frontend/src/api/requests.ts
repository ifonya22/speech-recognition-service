import axios from 'axios';

export interface VramResponse {
  modelName: string;
  requiredVram: string; 
}

export async function GetRequiredVram(): Promise<VramResponse | {}> {
  try {
    const response = await axios.get<VramResponse>(
      'http://localhost:8000/api/v1/models/required_vram'
    );
    return response.data;
  } catch (error) {
    console.error('Ошибка при запросе данных:', error);
    return {};
  }
}