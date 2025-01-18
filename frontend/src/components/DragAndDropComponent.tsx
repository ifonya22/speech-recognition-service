import React from 'react';
import { InboxOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { message, Upload } from 'antd';

const { Dragger } = Upload;

const props: UploadProps = {
  name: 'file',
  multiple: true,
  action: 'https://660d2bd96ddfa2943b33731c.mockapi.io/api/upload',
  accept: '.mp3,.wav,.flac,.m4a', 
  onChange(info) {
    const { status } = info.file;
    if (status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (status === 'done') {
      message.success(`${info.file.name} файл успешно загружен.`);
    } else if (status === 'error') {
      message.error(`${info.file.name} загрузка файла не удалась.`);
    }
  },
  onDrop(e) {
    console.log('Dropped files', e.dataTransfer.files);
  },
};

const DragAndDropComponent: React.FC = () => (
  <Dragger {...props}>
    <p className="ant-upload-drag-icon">
      <InboxOutlined />
    </p>
    <p className="ant-upload-text">Кликните или перетащите файлы сюда</p>
    <p className="ant-upload-hint">
      Возможные форматы: .mp3, .wav
    </p>
  </Dragger>
);

export default DragAndDropComponent;