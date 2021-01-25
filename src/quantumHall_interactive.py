import ipywidgets as widgets
from ipywidgets import interactive_output, Layout, HBox, VBox, Box, Label
from .quantumHall_draw import DrawQuantumHall
from .quantumHall import QuantumHall

class QuantumHallInteractive():
    def __init__(self,num_modes=2,num_terminals=2):
        self.num_modes = num_modes
        self.num_terminals = num_terminals

    def init_bar_widgets(self):
        # Widgets for chiralities
        self.chirality_wdgts = [widgets.Label(value='Chiralities:',
                                         layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for mode in range(self.num_modes):
            c = widgets.BoundedIntText( value=1, min=-1, max=1, step=2,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.chirality_wdgts.append( c )

        # Widgets for electrical charges
        self.charge_wdgts = [widgets.Label(value='Electrical Charges:',
                                         layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for mode in range(self.num_modes):
            c = widgets.BoundedFloatText( value=1.0, min=0.0, max=5.0, step=0.1,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.charge_wdgts.append( c )

        # Widgets for central charges
        self.cent_charge_wdgts = [widgets.Label(value='Central Charges:',
                                         layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for mode in range(self.num_modes):
            c = widgets.BoundedFloatText( value=1.0, min=0.0, max=5.0, step=0.1,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.cent_charge_wdgts.append( c )

        # Widgets for voltage at terminals
        self.voltage_wdgts = [widgets.Label(value='Voltage (in $\mu eV$) at:',
                                       layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for terminal in range(self.num_terminals):
            v = widgets.BoundedFloatText( value=0.0, min=-10.0, max=10.0, step=0.1,
                                     description=' terminal #'+str(terminal+1),
                                         layout = Layout(width='150px'),
                                         disabled=False)
            self.voltage_wdgts.append( v )

        # Widgets for temperature at terminals
        self.temperature_wdgts = [widgets.Label(value='Temperature (in $mK$) at:',
                                       layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for terminal in range(self.num_terminals):
            v = widgets.BoundedFloatText( value=50.0, min=0.0, max=1000.0, step=5.0,
                                     description=' terminal #'+str(terminal+1),
                                         layout = Layout(width='150px'),
                                         disabled=False)
            self.temperature_wdgts.append( v )


        self.num_modes_old = self.num_modes
        self.num_terminals_old = self.num_terminals
        #return chirality_wdgts, charge_wdgts, cent_charge_wdgts, voltage_wdgts, temperature_wdgts

    def take_widget_values(self):
        # Taking the chiralities
        self.chirality_vec = [self.chirality_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the charges
        self.charge_vec = [self.charge_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the central charges
        self.cent_charge_vec = [self.cent_charge_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the voltages
        self.voltage_vec = [self.voltage_wdgts[m].value for m in range(1,self.num_terminals+1) ]
        # Taking the temperatures
        self.temperature_vec = [self.temperature_wdgts[m].value for m in range(1,self.num_terminals+1) ]
        
        # Taking the conductivity coefficients
        self.charge_conduct_matrix =[ [ self.conduct_matrix_wdgt_max['Charge'][row][column].value 
                                  for row in range(2,self.num_modes+2)  ]
                                for column in range(1,self.num_modes+1)  ]

        self.heat_conduct_matrix =[ [ self.conduct_matrix_wdgt_max['Heat'][row][column].value 
                                  for row in range(2,self.num_modes+2)  ]
                                for column in range(1,self.num_modes+1)  ]

    def calculate_transport(self):
        qh = QuantumHall( chirality_vector=self.chirality_vec, 
                         charge_vector=self.charge_vec, charge_conduct_matrix = self.charge_conduct_matrix,
                        central_charge_vector=self.cent_charge_vec, heat_conduct_matrix=self.heat_conduct_matrix,
                     voltages=self.voltage_vec, temperatures = self.temperature_vec )
        
        # unit of electrical current will be picoAmpere
        self.charge_currents = qh.current_all_terminals('charge','SI')*1e12
        # unit of thermla current will be femtoWatts
        self.heat_currents = qh.current_all_terminals('charge','SI')*1e15
        
        if self.num_terminals>3:
            self.four_terminal_thermal_conductance = qh.four_terminal_conductance((1,3),(2,4), 'charge' )
            self.four_terminal_electrical_conductance = qh.four_terminal_conductance((1,3),(2,4), 'heat')
        
        self.two_terminal_thermal_conductance = qh.two_terminal_conductance('charge')
        self.two_terminal_electrical_conductance = qh.two_terminal_conductance('heat')
        
        
    def display_widgets_bar(self,num_terminals,num_modes):
        self.num_modes = num_modes
        self.num_terminals = num_terminals
        
        # updating mode widgets
        if self.num_modes_old < self.num_modes:
            for mode in range(self.num_modes_old,self.num_modes):
                # Updating chirality widgets
                c = widgets.BoundedIntText( value=1, min=-1, max=1, step=2,
                                         description=' mode #'+str(mode+1),
                                             layout = Layout(width='130px'),
                                             disabled=False)
                self.chirality_wdgts.append( c )

                # Updating charge widgets
                c = widgets.BoundedIntText( value=1, min=-1, max=1, step=2,
                                         description=' mode #'+str(mode+1),
                                             layout = Layout(width='130px'),
                                             disabled=False)
                self.charge_wdgts.append( c )

                # Updating central charge widgets
                c = widgets.BoundedIntText( value=1, min=-1, max=1, step=2,
                                         description=' mode #'+str(mode+1),
                                             layout = Layout(width='130px'),
                                             disabled=False)
                self.cent_charge_wdgts.append( c )

        elif self.num_modes_old> self.num_modes:
            del self.chirality_wdgts[self.num_modes+1:self.num_modes_old+1]
            del self.charge_wdgts[self.num_modes+1:self.num_modes_old+1]
            del self.cent_charge_wdgts[self.num_modes+1:self.num_modes_old+1]

        #horz_layout = Layout(dispaly='flex',flex_flow='row',overflow='scroll_hidden',width='70%')
        horz_layout = Layout()
        vert_layout = Layout(border='solid 1px',width='80%')
        #display( HBox(self.chirality_wdgts ,layout = layout )  )
        #display( HBox(self.charge_wdgts)  )
        #display( HBox(self.cent_charge_wdgts)  )
        display( VBox( [ HBox(self.chirality_wdgts,layout=horz_layout),
                        HBox(self.charge_wdgts,layout=horz_layout),
                        HBox(self.cent_charge_wdgts,layout=horz_layout) 
                       ] ,layout=vert_layout ) )
        
        if self.num_terminals_old < self.num_terminals:
            for terminal in range(self.num_terminals_old, self.num_terminals):
                # Updating voltage widgets
                v = widgets.BoundedFloatText( value=0.0, min=-10.0, max=10.0, step=0.1,
                                         description='terminal #'+str(terminal+1),
                                             layout = Layout(width='150px'),
                                             disabled=False)
                self.voltage_wdgts.append( v )

                # Updating temperature widgets
                v = widgets.BoundedFloatText( value=0.0, min=-10.0, max=10.0, step=0.1,
                                         description='terminal #'+str(terminal+1),
                                             layout = Layout(width='150px'),
                                             disabled=False)
                self.temperature_wdgts.append( v )

        elif self.num_terminals_old> self.num_terminals:
            del self.voltage_wdgts[self.num_terminals+1:self.num_terminals_old+1]
            del self.temperature_wdgts[self.num_terminals+1:self.num_terminals_old+1]


        display( VBox( [HBox(self.voltage_wdgts), HBox(self.temperature_wdgts) ] ,layout=vert_layout  ) )

        self.take_widget_values()
        self.calculate_transport()
        
        
        
        # Display the conduction matrices
        display( self.conduct_matrix_tab() )
        
        # Plot the Hall Bar
        qhbar = DrawQuantumHall( self.num_terminals, self.num_modes,  chirality_vec )
        qhbar.draw_bar()

        self.num_terminals_old, self.num_modes_old = self.num_terminals, self.num_modes
        #return voltage_wdgts

    def init_conduct_matrix_wdgt(self,quantity):
        size = '60px'
        ws = [widgets.Label(value='', layout=Layout(width=size),style={'description_width': 'initial'} )]
        ws = [ ws+[widgets.Label(value='Mode #'+str(c+1),
                                           layout=Layout(width=size)
                                 ,style={'description_width': 'initial'} ) for c in range(self.max_num_modes)] ]

        for row in range(self.max_num_modes):
            ws_row = [widgets.Label(value='Mode #'+str(row+1),
                                           layout=Layout(width=size),style={'description_width': 'initial'} )]
            for column in range(self.max_num_modes):
                w = widgets.BoundedFloatText( value=0.0, min=0.0, max=5.0, step=0.1,
                                             layout = Layout(width=size),
                                             disabled=(column <= row) )
                ws_row.append(w)
            ws.append(ws_row)

        for row in range(1,self.max_num_modes):
            for column in range(row,self.max_num_modes):
                widgets.link( (ws[row][column],'value'),(ws[column][row],'value')  )

        
        title_wdgt = [  widgets.Label(value='', layout=Layout(width='70px'),
                                       style={'description_width': 'initial'} )  ,
                    widgets.Label(value=quantity+' Conductivity Matrix',
                                  layout=Layout(width='auto',height='auto', font_size=10),
                                  style={'description_width': 'initial'} )
                        ]
        
        self.conduct_matrix_wdgt_max[quantity] = [title_wdgt]+ws
        
    def init_both_conduct_matrix_wdgt(self):
        self.conduct_matrix_wdgt_max = {}
        self.init_conduct_matrix_wdgt('Charge')
        self.init_conduct_matrix_wdgt('Heat')
    
    def updated_conduct_matrix_wdgt(self,quantity):
        #row=
        #box = HBox( [self.conduct_matrix_wdgt_max[quantity][row][column]  
         #                   for column in range(self.num_modes+1)  ] )
        
        box = VBox( [HBox( self.conduct_matrix_wdgt_max[quantity][0] )] +
                   [HBox( [self.conduct_matrix_wdgt_max[quantity][row][column]  
                            for column in range(self.num_modes+1)  ] ) 
                     for row in range(1,self.num_modes+2)] )
        return box
    
    def conduct_matrix_wdgt(self,quantity):
        """
        Constructs the matrix everytime from scratch
        """
        
        size = '60px'
        ws = [widgets.Label(value='', layout=Layout(width=size),style={'description_width': 'initial'} )]
        ws = [ ws+[widgets.Label(value='Mode #'+str(c+1),
                                           layout=Layout(width=size),style={'description_width': 'initial'} ) for c in range(self.num_modes)] ]

        for row in range(self.num_modes):
            ws_row = [widgets.Label(value='Mode #'+str(row+1),
                                           layout=Layout(width=size),style={'description_width': 'initial'} )]
            for column in range(self.num_modes):
                w = widgets.BoundedFloatText( value=0.0, min=0.0, max=5.0, step=0.1,
                                             layout = Layout(width=size),
                                             disabled=(column <= row) )
                ws_row.append(w)
            ws.append(ws_row)

        for row in range(1,self.num_modes):
            for column in range(row,self.num_modes):
                widgets.link( (ws[row][column],'value'),(ws[column][row],'value')  )

        title = HBox( [  widgets.Label(value='', layout=Layout(width='70px'),
                                       style={'description_width': 'initial'} )  ,
                    widgets.Label(value=quantity+' Conductivity Matrix',
                                  layout=Layout(width='auto',height='auto', font_size=10),
                                  style={'description_width': 'initial'} )
                        ] )
        box = VBox( [ title ]+[HBox(ws[w]) for w in range(self.num_modes+1)] )
        return box

    def conduct_matrix_tab(self):
        charge_cond_box = self.updated_conduct_matrix_wdgt( 'Charge')
        heat_cond_box = self.updated_conduct_matrix_wdgt( 'Heat')
        tab = widgets.Tab( children=[ charge_cond_box,heat_cond_box ], layout=Layout(width='70%') )
        tab.set_title(0,'Charge conductivity matrix')
        tab.set_title(1,'Heat conductivity matrix')
        return tab
    
    def observe_widget_values(self):
        pass

    def display_all(self):
        #self.num_terminals_old, self.num_modes_old = 2,1
        self.max_num_modes = 10
        num_terminals_wdgt = widgets.BoundedIntText( value=self.num_terminals, min=2, max=12, step=1,
                                            description='Number of Terminals:', disabled=False,
                                            layout=Layout(width='200px'),style={'description_width': 'initial'})
        num_modes_wdgt = widgets.BoundedIntText( value=self.num_modes, min=1, max=self.max_num_modes, step=1,
                                        description='Number of Modes:', disabled=False,
                                       layout=Layout(width='200px'),style={'description_width': 'initial'} )

        #chirality_wdgts, charge_wdgts, cent_charge_wdgts, voltage_wdgts,temperature_wdgts = 
        self.init_bar_widgets()
        self.init_both_conduct_matrix_wdgt()

        out = interactive_output( self.display_widgets_bar,
                                { 'num_terminals' : num_terminals_wdgt , 'num_modes' : num_modes_wdgt  }
                                )
        display( HBox( [num_modes_wdgt,num_terminals_wdgt])  , out)
        
        self.observe_widget_values()
