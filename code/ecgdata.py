import glob
import os

class EcgData():
    '''
    get data from path
    params:
        self.data: np.array, shape=(id,lead_num, sample_num)
        self.label: np.array, shape=(id, label_num)
    
    def:
        __getitem__(idx) -> np.array, shape=(lead_num, sample_num) or (id_num, lead_num, sample_num)
        split_ecgdata(train_rate: float) -> (train_data, train_label, val_data, val_label)
    '''
    def __init__(self, path:str, data_name:str):
        '''
        params:
            data_name: str, 'mimic' or 'mimic_demo'
            path: str, 
                ex) '/content/physionet.org/files/mimic-iv-ecg-demo/0.1/files/' if data_name=='mimic_demo'
                ex) '/content/physionet.org/files/mimic-iv-ecg/0.1/files/' if data_name=='mimic'
        '''
        self.path = path
        self.data_name = data_name
        
        self.data, self.label = np.array([]), np.array([])
        if self.data_name == 'mimic':
            self.data = self._get_data_from_mimic(self.path)
        elif self.data_name == 'mimic_demo':
            self.data = self._get_data_from_mimic_demo(self.path)

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def _get_data_from_mimic(self, path:str, is_demo:bool=False):
        root_path = path
        if is_demo:
            p_file_names = glob.glob(os.path.join(root_path,'p*'))
        else:
            p_file_names = glob.glob(os.path.join(root_path,'p*','p*'))
    
        data_list = []
        for p_file_name in p_file_names:
            s_file_names = glob.glob(os.path.join(p_file_name,'s*'))
            for s_file_name in s_file_names:
                hea_file_name = glob.glob(os.path.join(s_file_name,'*.hea'))[0]
                dat_file_name = glob.glob(os.path.join(s_file_name,'*.dat'))[0]
                _v,_lead_num, _rate = [], None, None  # mV, num of leads,sample rate
                _v, _lead_num, _rate = self._read_hea_file(hea_file_name)
                with open(dat_file_name, 'rb') as f:
                    data = np.fromfile(f, dtype=np.int16, sep = '')
                    data_list.append(data.reshape(-1,_lead_num).T/_v) ##<===　/_vはあってる？？
        return np.array(data_list)


    def _get_data_from_mimic_demo(self, path:str):
        return self._get_data_from_mimic(path, is_demo=True)


    def _read_hea_file(self, file_name:str)-> tuple[np.array, int, int]:
        _v,_lead_num,_rate = [], None, None  # mV, num of leads,sample rate
        with open(file_name,"r") as f:
            _f = f.readlines()
            _lead_num,_rate = _f[0].split(" ")[1:3]
            _lead_num, _rate = int(_lead_num),int(_rate)
            for x in _f[1:1+_lead_num]:
                xx = x.split(" ")[2]
                _v.append(int(xx[:xx.find(".")]))
        _v = np.array(_v).reshape(_lead_num,1)
        return _v, _lead_num, _rate


    def split_ecgdata(self, train_rate: float=0.8) -> tuple[np.array, np.array, np.array, np.array]:
        pass
