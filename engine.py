import PySide6.QtCore as Qc
import time
import math

WIDTH = 1600
HEIGHT = 900
G = 10000
OBJECTS = []

class Object:
    def __init__(self,mass,r,p_x,p_y,v_x,v_y,color):
        self.mass = mass
        self.r = r
        self.p_x = p_x
        self.p_y = p_y
        self.v_x = v_x
        self.v_y = v_y
        self.color = color
        self.update_mechanical_value()

    def update_positional_value(self,width,height,fps):
        self.p_x += self.v_x/fps
        self.p_y += self.v_y/fps
        if (-width+self.r > self.p_x):
            self.p_x = -width+self.r
            self.v_x = -self.v_x
            self.update_mechanical_value()
        elif (self.p_x > width-self.r):
            self.p_x = width-self.r
            self.v_x = -self.v_x
            self.update_mechanical_value()
        if (-height+self.r > self.p_y):
            self.p_y = -height+self.r
            self.v_y = -self.v_y
            self.update_mechanical_value()
        elif (self.p_y > height-self.r):
            self.p_y = height-self.r
            self.v_y = -self.v_y
            self.update_mechanical_value()

    def update_velocity_value(self):
        self.v_x = self.m_x/self.mass
        self.v_y = self.m_y/self.mass

    def update_mechanical_value(self):
        self.m_x = self.mass*self.v_x
        self.m_y = self.mass*self.v_y
        self.k_x = 0.5*self.mass*self.v_x**2
        self.k_y = 0.5*self.mass*self.v_y**2

    def affected(self,m_x,m_y):
        self.m_x += m_x
        self.m_y += m_y
        self.update_velocity_value()
        self.update_mechanical_value()

    def crash(obj1,obj2):
        distance = ((obj1.p_x-obj2.p_x)**2+(obj1.p_y-obj2.p_y)**2)**0.5
        """
        moment = ((obj1.m_x-obj2.m_x)**2+(obj1.m_y-obj2.m_y)**2)**0.5
        obj1_theata = math.atan2(obj2.p_y-obj1.p_y,obj2.p_x-obj1.p_x) - math.atan2(obj1.m_y-obj2.m_y,obj1.m_x-obj2.m_x)
        obj1_theata = obj1_theata + 2*math.pi if -math.pi >= obj1_theata else obj1_theata - 2*math.pi if obj1_theata >= math.pi else obj1_theata
        obj2_theata = math.atan2(obj1.p_y-obj2.p_y,obj1.p_x-obj2.p_x) - math.atan2(obj2.m_y-obj1.m_y,obj2.m_x-obj1.m_x)
        obj2_theata = obj2_theata + 2*math.pi if -math.pi >= obj2_theata else obj2_theata - 2*math.pi if obj2_theata >= math.pi else obj2_theata
        if distance<=obj1.r+obj2.r and -math.pi/2 < obj1_theata < math.pi/2 and -math.pi/2 < obj2_theata < math.pi/2:
            obj1_tan = math.atan2(obj2.p_y-obj1.p_y,obj2.p_x-obj1.p_x)
            obj1_affect_x = math.cos(obj1_tan)*math.cos(obj1_theata)*moment
            obj1_affect_y = math.sin(obj1_tan)*math.cos(obj1_theata)*moment
            obj2_tan = math.atan2(obj1.p_y-obj2.p_y,obj1.p_x-obj2.p_x)
            obj2_affect_x = math.cos(obj2_tan)*math.cos(obj2_theata)*moment
            obj2_affect_y = math.sin(obj2_tan)*math.cos(obj2_theata)*moment
            """
        dot_m_p_obj1 = (obj2.p_x-obj1.p_x)*(obj1.m_x-obj2.m_x)+(obj2.p_y-obj1.p_y)*(obj1.m_y-obj2.m_y)
        dot_m_p_obj2 = (obj1.p_x-obj2.p_x)*(obj2.m_x-obj1.m_x)+(obj1.p_y-obj2.p_y)*(obj2.m_y-obj1.m_y)
        if distance<=obj1.r+obj2.r and dot_m_p_obj1 > 0 and dot_m_p_obj2 > 0:
            cos_obj1 = dot_m_p_obj1/distance#/(obj1.m_x**2+obj1.m_y**2)**0.5
            obj1_tan = math.atan2(obj2.p_y-obj1.p_y,obj2.p_x-obj1.p_x)
            obj1_affect_x = math.cos(obj1_tan)*cos_obj1
            obj1_affect_y = math.sin(obj1_tan)*cos_obj1

            cos_obj2 = dot_m_p_obj2/distance#/(obj2.m_x**2+obj2.m_y**2)**0.5
            obj2_tan = math.atan2(obj1.p_y-obj2.p_y,obj1.p_x-obj2.p_x)
            obj2_affect_x = math.cos(obj2_tan)*cos_obj2
            obj2_affect_y = math.sin(obj2_tan)*cos_obj2
            #print(obj1_affect_x,obj2_affect_x,obj1_affect_y,obj2_affect_y)
            #"""
            obj1.affected(obj2_affect_x,obj2_affect_y)
            obj2.affected(obj1_affect_x,obj1_affect_y)

    def gravite(obj1,obj2,g,fps):
        force = g*obj1.mass*obj2.mass/((obj1.p_x-obj2.p_x)**2+(obj1.p_y-obj2.p_y)**2)
        moment = force/fps
        obj1_tan = math.atan2(obj2.p_y-obj1.p_y,obj2.p_x-obj1.p_x)
        obj1_affected_x = math.cos(obj1_tan)*moment
        obj1_affected_y = math.sin(obj1_tan)*moment
        obj2_tan = math.atan2(obj1.p_y-obj2.p_y,obj1.p_x-obj2.p_x)
        obj2_affected_x = math.cos(obj2_tan)*moment
        obj2_affected_y = math.sin(obj2_tan)*moment
        obj1.affected(obj1_affected_x,obj1_affected_y)
        obj2.affected(obj2_affected_x,obj2_affected_y)
        #print(obj1_affected_x,obj1_affected_y)
        #print(obj2_affected_x,obj2_affected_y)




class World():
    def __init__(self,width=WIDTH,height=HEIGHT,g=G,objects=OBJECTS):
        self.width = width
        self.height = height
        self.g = g
        self.objects = objects

    def update(self,fps):
        for i in range(len(self.objects)):
            self.objects[i].update_positional_value(self.width,self.height,fps)
        for i in range(len(self.objects)-1):
            for j in range(i+1,len(self.objects)):
                Object.crash(self.objects[i],self.objects[j])
                Object.gravite(self.objects[i],self.objects[j],self.g,fps)
        