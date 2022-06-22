class MovableObject:
    """Basic class which handles and object's movement
    NOTE: Does not handle image"""
    
    def __init__(self, pos, vel, friction, max_vel):
        self.pos = pos
        self.friction = friction
        self.vel = vel
        self.max_vel = max_vel

    def update(self):
        for axis in range(2):
            # NOTE: self.vel can be inaccurate at the end but when
            # of the function because friction is applied to it after it  
            # has reached its max it is additioned to self.pos[axis], it  
            # is accurate since we set it to its max before that line
            if not self.max_vel is None: 
                if self.vel[axis] > self.max_vel:
                    self.vel[axis] = self.max_vel
                elif self.vel[axis] < -self.max_vel:
                    self.vel[axis] = -self.max_vel
            self.pos[axis] += self.vel[axis]
            if self.vel[axis] > 0:
                self.vel[axis] -= self.friction
                if self.vel[axis] < 0:
                    self.vel[axis] = 0
            else:
                self.vel[axis] += self.friction
                if self.vel[axis] > 0:
                    self.vel[axis] = 0