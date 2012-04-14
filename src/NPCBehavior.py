import random
import GameState

STATE_DISABLED = 0
STATE_IDLE = 1
STATE_CHASE = 2
STATE_ATTACK = 3
STATE_FLEE = 4
STATE_DEAD = 5

#npc needs hide function
#

class NPCBehavior:
    def __init__(self,npc):
        assert(npc != None)
        self.npc = npc
        self.state = None
        self.nextState = STATE_IDLE
        self.target = None
        self.noodleTick = 0
        self.pathList = []
    
    def updateState(self):
        if self.nextState:
            self.state = self.nextState
            self.nextState = None
    
    def activity(self):
        if not PLAYER_ON_SAME_MAP:
            return
        
        self.noodleTick += 1
        if(self.noodleTick > 360)
            self.noodleTick = 0
            self.updateState()
        else:
            return
        
        assert(self.npc != None)
        assert(self.state != None)
        
        if self.state == STATE_CHASE:
            if self.npc.sqDistanceFrom(self.target) < 33*33:
                self.nextState = STATE_ATTACK
            
            if pathLists.empty():
                self.nextState = STATE_IDLE
                self.target = None
            else:
                moveTo(pathLists.pop())
                
        elif self.state = STATE_ATTACK:
            if self.npc.sqDistanceFrom(self.target) >= 33*33:
                self.nextState = STATE_CHASE
                
        elif self.state == STATE_IDLE:
            self.target = GameState.player
            self.nextState = STATE_CHASE
    
    def moveTick(self):
    
    def rethinkPath(self,x,y):
        paths = []
        visited = []
        foundPath = explore(self.npc.getTilePos(),target.getTilePos(),paths,visited)
        if foundPath:
            self.pathList = paths
        else:
            self.pathList = []
    
    def impassable(self,x,y):
        return (GameState.getCurrentAtMap[x][y] != '.')
    
    def explore(self,cur,end,pathList,visited):
        if cur == end:
            return True
        else:
            visited.append(cur)
            print cur,"has been visited"
            # current direction priority with respect to end position
            left = [0,(cur[0]-1,cur[1])]
            right = [0,(cur[0]+1,cur[1])]
            up = [0,(cur[0],cur[1]+1)]
            down = [0,(cur[0],cur[1]-1)]
            
            xdif = end[1] - cur[1]
            ydif = end[0] - cur[0]
            
            if xdif > 0:
                left[0] += 1
            elif xdif < 0:
                right[0] += 1
            
            if ydif > 0:
                down[0] += 1
            elif xdif < 0:
                up[0] += 1
            
            pTiles = sorted([left,right,up,down], key=itemgetter(0), reverse=True)
            result = []
            
            for nextTile in pTiles:
                if impassable(nextTile[1],visited):
                    result.append((False,nextTile[1]))
                    print "  ",nextTile[1],"impassable"
                else:
                    good = explore(nextTile[1],end,pathList,visited)
                    result.append((good,nextTile[1]))
                    print "  ",nextTile[1],"passable"
                    if good:
                        break
            
            for explored_tile in result:
                if explored_tile[0] == True:
                pathList.append(explored_tile[1])
                return True
            
            return False

        
