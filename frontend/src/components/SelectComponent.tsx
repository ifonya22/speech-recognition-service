import React, { useEffect, useState } from 'react';
import { Select, Spin } from 'antd';
import { GetRequiredVram } from '../api/requests';

interface Option {
  value: string;
  label: string;
}

const SelectComponent: React.FC = () => {
  const [options, setOptions] = useState<Option[]>([]);
  const [loading, setLoading] = useState<boolean>(true); 

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true); 
        const data = await GetRequiredVram();

        const formattedOptions = Object.entries(data).map(([key, value]) => ({
          value: key, 
          label: `${key} (${value})`, 
        }));
        setOptions(formattedOptions);
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      } finally {
        setLoading(false); 
      }
    }

    fetchData();
  }, []);

  const onChange = (value: string) => {
    console.log(`selected ${value}`);
  };

  const onSearch = (value: string) => {
    console.log('search:', value);
  };

  if (loading) {
    return <Spin tip="Загрузка..." />;
  }

  return (
    <Select
      showSearch
      placeholder="Выберите модель"
      optionFilterProp="label"
      onChange={onChange}
      onSearch={onSearch}
      options={options}
      notFoundContent="Нет доступных данных" 
      style={{ width: '150px' }}
    />
  );
};

export default SelectComponent;
