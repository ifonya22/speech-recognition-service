import React from 'react';
import { Input } from 'antd';

const { TextArea } = Input;

const TextAreaComponent: React.FC = () => (
  <>
    <br />
    <TextArea rows={4} />
  </>
);

export default TextAreaComponent;