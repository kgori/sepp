'''
Created on Nov 26, 2012

@author: smirarab
'''
import os
import pickle
import sys
import threading
from sepp import get_logger

_LOG = get_logger(__name__)

class CheckPointState(object):
    '''
    The current state as relevant to the checkpointign feature
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.root_problem = None
        
def save_checkpoint(checkpoint_manager):
    #assert os.path.exists(self.checkpoint_path)
    if checkpoint_manager.is_checkpointing:
        _LOG.info("Checkpoint is being updated: %s" %str(checkpoint_manager.checkpoint_state.root_problem))
        currenlimit = sys.getrecursionlimit()
        sys.setrecursionlimit(100000)
        pickle.dump(checkpoint_manager.checkpoint_state, open(checkpoint_manager.checkpoint_path,"w"))
        sys.setrecursionlimit(currenlimit)
        _LOG.info("Checkpoint Saved to: %s" %str(checkpoint_manager.checkpoint_path))
        checkpoint_manager.timer = threading.Timer(3600, save_checkpoint, args={checkpoint_manager})
        checkpoint_manager.timer.setDaemon(True)
        checkpoint_manager.timer.start() 
            
class CheckPointManager:
    
    def __init__(self, checkpoint_file):            
        self.checkpoint_path = checkpoint_file
        self.checkpoint_state = None
        self.is_recovering = False
        self.is_checkpointing = False
        self.timer = None
        self._init_state_and_file()

    def _init_state_and_file(self):
        if self.checkpoint_path is None:
            return                    
        if not os.path.exists(self.checkpoint_path):
            open(self.checkpoint_path,"w").close()       
            self.checkpoint_state = CheckPointState()
            self.is_checkpointing = True
        else:                            
            self.is_recovering = True
            self.is_checkpointing = True
                                
    def restore_checkpoint(self):
        _LOG.info("Checkpoint is being restored: %s" %str(self.checkpoint_path))
        assert os.path.exists(self.checkpoint_path)
        self.checkpoint_state = pickle.load(open(self.checkpoint_path))        
        _LOG.info("Checkpoint restore finished: %s" %str(self.checkpoint_state.root_problem))
    
    def remove_checkpoint_file(self):
        os.remove(self.checkpoint_path)
        
    def start_checkpointing(self, root_problem):
        if self.is_checkpointing:
            self.checkpoint_state.root_problem = root_problem 
            save_checkpoint(self)
            
    def stop_checkpointing(self):
        self.is_checkpointing = False
        if self.timer is not None:
            self.timer.cancel()
        self.remove_checkpoint_file()
        
#    def backup_temp_directory(self, path):
#        assert(os.path.exists(path))
#        idx = 0
#        while os.path.exists("%s_back-%d" %(path,idx)): idx += 1                                        
#        new_name = "%s_back-%d" %(path,idx)
#        os.rename(path, new_name)
#        return new_name  