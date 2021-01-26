import numpy as np
import matplotlib as mpl
import matplotlib.patches as mpat
import matplotlib.pyplot as plt

class DrawQuantumHall():
    def __init__(self,num_terminals=2,num_modes=2,chirality_vector=None,charge_vector=None):
        self.Lx = 20
        self.Ly = 10
        #self.bar_plt = self.init_figure()
        self.num_modes = num_modes
        self.num_terminals = num_terminals
        #self.draw_QHall_bar(self.num_terminals_0,3)
        #self.display_gizmos()

        if chirality_vector is None:
            self.chirality_vector = np.ones(self.num_modes, dtype=int)
        elif len(chirality_vector)!= self.num_modes:
            raise TypeError('The length of the chirality vector does not match the number of modes')
        else:
            self.chirality_vector = np.array(chirality_vector)

        if charge_vector is None:
            self.charge_vector = np.ones(self.num_modes, dtype=int)
        elif len(charge_vector)!= self.num_modes:
            raise TypeError('The length of the charge vector does not match the number of modes')
        else:
            self.charge_vector = np.array(charge_vector)
            
        self.init_plot_objects()

    def init_plot_objects(self):
        self.mode_object_list = None


    def draw_one_mode(self, plt_obj ,margin ,color,chirality):
        bottom_y = -self.Ly + margin
        top_y = self.Ly-margin
        left_x = -self.Lx+margin
        right_x = self.Lx-margin

        middle_x = 0
        middle_y = 0
        #color=color
        arrow_size = 0.4
        linestyle = '-'

        mode_obj = []
        # top line
        mode_obj.append( plt_obj.plot( (left_x,right_x),(top_y,top_y), color=color,ls=linestyle ) )
        mode_obj.append( plt_obj.arrow( middle_x,top_y,arrow_size*chirality,0 ,shape='full',
                      length_includes_head=True,head_width=arrow_size,overhang=0.5,color=color) )

        mode_obj.append(plt_obj.plot( (right_x,right_x),(top_y,bottom_y), color=color,ls=linestyle ) )
        mode_obj.append(plt_obj.arrow( right_x,middle_y,0,-arrow_size*chirality ,shape='full',
                      length_includes_head=True,head_width=arrow_size,overhang=0.5,color=color) )

        mode_obj.append(plt_obj.plot( (right_x,left_x),(bottom_y,bottom_y), color=color,ls=linestyle ) )
        mode_obj.append(plt_obj.arrow( middle_x,bottom_y,-arrow_size*chirality,0 ,shape='full',
                      length_includes_head=True,head_width=arrow_size,overhang=0.5,color=color))

        mode_obj.append(plt_obj.plot( (left_x,left_x),(bottom_y,top_y), color=color,ls=linestyle ) )
        mode_obj.append(plt_obj.arrow( left_x,middle_y,0,arrow_size*chirality ,shape='full',
                      length_includes_head=True,head_width=arrow_size,overhang=0.5,color=color))
        
        return mode_obj


    def draw_modes(self ):
        if self.mode_object_list is not None:
            del self.mode_object_list
        plt_obj = self.plt_obj
        mode_margin = 0.5
        mode_distance = 0.5
        cmap = mpl.cm.get_cmap('viridis')
        max_num_modes = 10
        mode_object_list = [] 
        for mode in range( self.num_modes ):
            color = cmap(mode/max_num_modes)
            mode_object_list.append( self.draw_one_mode(plt_obj,mode_margin+mode*mode_distance,color, self.chirality_vector[mode] ) )
            
        self.mode_object_list = mode_object_list

    def update_mode(self):
        pass
    
    def update_value(self, var , value ):
        if isinstance(var,str):
            exec( 'self.'+var+'='+ str(value) )
        else:
            print('Warning: var should be a string. No value has been changed.')
    
    def draw_terminals(self  ):
        plt_obj = self.plt_obj
        sides = 4
        num_terms_side = [0,0,0,0]
        side=0
        for terminal in range(self.num_terminals):
            num_terms_side[side] += 1
            side = (side+1)%sides


        terminals_quota = 0.5
        terminal_color = (0.5,0.5,0.9,0.8)
        terminal_height = self.Ly/4

        ax = plt_obj.gca()

        terminal_count = 1

        # Left side
        side = 0
        if num_terms_side[side]!=0:
            terminal_width_y = 2*self.Ly/num_terms_side[side]*terminals_quota
            inter_terminal_distance = 2*self.Ly*(1-terminals_quota)/(1+num_terms_side[side]  )
            for terminal in range( num_terms_side[side] ):
                bottom_left_corner = (-self.Lx-terminal_height,-self.Ly+inter_terminal_distance+terminal*(terminal_width_y+inter_terminal_distance)  )
                rect = mpat.Rectangle( bottom_left_corner ,
                                      terminal_height,terminal_width_y,
                                       facecolor=terminal_color, edgecolor='black' )
                ax.add_patch(rect)

                x,y = bottom_left_corner
                x += terminal_height/2
                y += terminal_width_y/2
                plt_obj.text( x,y, 'Terminal #'+str(terminal_count),rotation='vertical',ha='center', va='center' )
                terminal_count += 1

        # Top side
        side = 2
        if num_terms_side[side]!=0:
            terminal_width_x = 2*self.Lx/num_terms_side[side]*terminals_quota
            inter_terminal_distance = 2*self.Lx*(1-terminals_quota)/(1+num_terms_side[side]  )
            for terminal in range( num_terms_side[side] ):
                bottom_left_corner = (-self.Lx+inter_terminal_distance+terminal*(terminal_width_x+inter_terminal_distance) , self.Ly )
                rect = mpat.Rectangle( bottom_left_corner ,
                                       terminal_width_x,terminal_height,
                                       facecolor=terminal_color, edgecolor='black'  )
                ax.add_patch(rect)

                x,y = bottom_left_corner
                y += terminal_height/2
                x += terminal_width_x/2
                plt_obj.text( x,y, 'Terminal #'+str(terminal_count),ha='center', va='center' )
                terminal_count += 1


        # Right side
        side = 1
        if num_terms_side[side]!=0:
            terminal_width_y = 2*self.Ly/num_terms_side[side]*terminals_quota
            inter_terminal_distance = 2*self.Ly*(1-terminals_quota)/(1+num_terms_side[side]  )
            for terminal in range( num_terms_side[side]-1,-1,-1 ):
                bottom_left_corner = (self.Lx,-self.Ly+inter_terminal_distance+terminal*(terminal_width_y+inter_terminal_distance)  )
                rect = mpat.Rectangle( bottom_left_corner ,
                                      terminal_height,terminal_width_y,
                                      facecolor=terminal_color, edgecolor='black' )
                ax.add_patch(rect)

                x,y = bottom_left_corner
                x += terminal_height/2
                y += terminal_width_y/2
                plt_obj.text( x,y, 'Terminal #'+str(terminal_count),rotation=-90,ha='center', va='center' )
                terminal_count += 1


        # Bottom side
        side = 3
        if num_terms_side[side]!=0:
            terminal_width_x = 2*self.Lx/num_terms_side[side]*terminals_quota
            inter_terminal_distance = 2*self.Lx*(1-terminals_quota)/(1+num_terms_side[side]  )
            for terminal in range( num_terms_side[side]-1, -1, -1):
                bottom_left_corner = (-self.Lx+inter_terminal_distance+terminal*(terminal_width_x+inter_terminal_distance) , -self.Ly-terminal_height )
                rect = mpat.Rectangle( bottom_left_corner ,
                                      terminal_width_x, terminal_height,
                                      facecolor=terminal_color, edgecolor='black' )
                ax.add_patch(rect)

                x,y = bottom_left_corner
                y += terminal_height/2
                x += terminal_width_x/2
                plt_obj.text( x,y, 'Terminal #'+str(terminal_count),ha='center', va='center' )
                terminal_count += 1


    def draw_bar(self ):
        outer_margin = 4

        plt.figure( figsize=(15,10) )
        self.plt_obj = plt
        ax = plt.gca()
        ax.set_xlim(-self.Lx-outer_margin,self.Lx+outer_margin)
        ax.set_ylim(-self.Ly-outer_margin,self.Ly+outer_margin)


        self.draw_modes( )

        rect = mpat.Rectangle( (-self.Lx,-self.Ly), 2*self.Lx,2*self.Ly,color=(0.8,0.8,0.9,0.5) )
        ax.add_patch(rect)
        filling_fraction = abs( np.dot(self.chirality_vector, self.charge_vector  ) )
        plt.text( 0,0, 'Quantum Hall bar at filling fraction '+'{:.2f}'.format( filling_fraction ),
                  fontfamily='sans-serif',fontsize='xx-large',ha='center', va='center' )

        self.draw_terminals()
        plt.axis('off')
