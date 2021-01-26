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
        for mode in range(self.max_num_modes):
            c = widgets.BoundedIntText( value=1, min=-1, max=1, step=2,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.chirality_wdgts.append( c )

        # Widgets for electrical charges
        self.charge_wdgts = [widgets.Label(value='Electrical Charges:',
                                         layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for mode in range(self.max_num_modes):
            c = widgets.BoundedFloatText( value=1.0, min=0.0, max=5.0, step=0.1,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.charge_wdgts.append( c )

        # Widgets for central charges
        self.cent_charge_wdgts = [widgets.Label(value='Central Charges:',
                                         layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for mode in range(self.max_num_modes):
            c = widgets.BoundedFloatText( value=1.0, min=0.0, max=5.0, step=0.1,
                                     description=' mode #'+str(mode+1),
                                         layout = Layout(width='130px'),
                                         disabled=False)
            self.cent_charge_wdgts.append( c )

        # Widgets for voltage at terminals
        self.voltage_wdgts = [widgets.Label(value='Voltage (in $\mu eV$) at:',
                                       layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for terminal in range(self.max_num_terminals):
            v = widgets.BoundedFloatText( value=0.0, min=-10.0, max=10.0, step=0.1,
                                     description=' terminal #'+str(terminal+1),
                                         layout = Layout(width='150px'),
                                         disabled=False)
            self.voltage_wdgts.append( v )

        # Widgets for temperature at terminals
        self.temperature_wdgts = [widgets.Label(value='Temperature (in $mK$) at:',
                                       layout=Layout(width='150px'),style={'description_width': 'initial'} )]
        for terminal in range(self.max_num_terminals):
            v = widgets.BoundedFloatText( value=50.0, min=0.0, max=1000.0, step=5.0,
                                     description=' terminal #'+str(terminal+1),
                                         layout = Layout(width='150px'),
                                         disabled=False)
            self.temperature_wdgts.append( v )


        #self.num_modes_old = self.num_modes
        #self.num_terminals_old = self.num_terminals
        #return chirality_wdgts, charge_wdgts, cent_charge_wdgts, voltage_wdgts, temperature_wdgts

    def take_widget_values(self):
        # Taking the chiralities
        self.chirality_vector = [self.chirality_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the charges
        self.charge_vector = [self.charge_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the central charges
        self.cent_charge_vector = [self.cent_charge_wdgts[m].value for m in range(1,self.num_modes+1) ]
        # Taking the voltages
        self.voltages = [self.voltage_wdgts[m].value for m in range(1,self.num_terminals+1) ]
        # Taking the temperatures
        self.temperatures = [self.temperature_wdgts[m].value for m in range(1,self.num_terminals+1) ]
        
        # Taking the conductivity coefficients
        self.charge_conduct_matrix =[ [ self.conduct_matrix_wdgt_max['Charge'][row][column].value 
                                  for row in range(2,self.num_modes+2)  ]
                                for column in range(1,self.num_modes+1)  ]

        self.heat_conduct_matrix =[ [ self.conduct_matrix_wdgt_max['Heat'][row][column].value 
                                  for row in range(2,self.num_modes+2)  ]
                                for column in range(1,self.num_modes+1)  ]

    def calculate_transport(self):
        qh = QuantumHall( chirality_vector=self.chirality_vector, 
                         charge_vector=self.charge_vector, 
                         charge_conduct_matrix = self.charge_conduct_matrix,
                        central_charge_vector=self.cent_charge_vector,
                         heat_conduct_matrix=self.heat_conduct_matrix,
                     voltages=self.voltages, temperatures = self.temperatures )

        # unit of electrical current will be picoAmpere
        self.charge_currents = qh.current_all_terminals('charge','SI')*1e12
        # unit of thermla current will be femtoWatts
        self.heat_currents = qh.current_all_terminals('charge','SI')*1e15
        
        if self.num_terminals>3:
            self.four_terminal_electrical_conductance = qh.four_terminal_conductance((1,3),(2,4), 'charge' )
            self.four_terminal_thermal_conductance = qh.four_terminal_conductance((1,3),(2,4), 'heat')
        else:
            self.four_terminal_thermal_conductance = 0
            self.four_terminal_electrical_conductance = 0
        
        self.two_terminal_electrical_conductance = qh.two_terminal_conductance((1,2),'charge')
        self.two_terminal_thermal_conductance = qh.two_terminal_conductance( (1,2), 'heat')
        
    def update_transport(self):
        pass
        
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

    def conduct_matrix_tabs(self):
        charge_cond_box = self.updated_conduct_matrix_wdgt( 'Charge')
        heat_cond_box = self.updated_conduct_matrix_wdgt( 'Heat')
        tab = widgets.Tab( children=[ charge_cond_box,heat_cond_box ], layout=Layout(width='50%') )
        tab.set_title(0,'Charge conductivity matrix')
        tab.set_title(1,'Heat conductivity matrix')
        return tab
    
    def conductance_results_box(self):
        entry_width = '250px'
        label_width = '150px'
        box_title = [ widgets.Label(value='', layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} )  ,
                     widgets.Label(value='Conductance results', layout=Layout(width=entry_width ),
                                       style={'description_width': 'initial'} )]
        column_labels =[ widgets.Label(value='', layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} )  ,
                        widgets.Label(value='Electrical ($e^2/h$)', layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} ),
                         widgets.Label(value='Thermal ($(\pi k_B)^2/3h$)', layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} ) ]
        self.two_terminal_row = [ widgets.Label(value='Two-terminal', layout=Layout(width=label_width),
                                       style={'description_width': 'initial'} ),
                            widgets.Label(value= '{:.2f}'.format(self.two_terminal_electrical_conductance),
                                  layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} ), 
                            widgets.Label(value= '{:.2f}'.format(self.two_terminal_thermal_conductance),
                                  layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} ) ]
        self.four_terminal_row = [ widgets.Label(value='Four-terminal', layout=Layout(width=label_width),
                                       style={'description_width': 'initial'} ),
                             widgets.Label(value= '{:.2f}'.format(self.four_terminal_electrical_conductance),
                                  layout=Layout(width=entry_width),
                                       style={'description_width': 'initial'} ), 
                            widgets.Label(value= '{:.2f}'.format(self.four_terminal_thermal_conductance),
                                  layout=Layout(width=entry_width ),
                                       style={'description_width': 'initial'} ) ]
        results_box_wdgt = VBox( [ HBox( box_title ), HBox(column_labels), 
                                  HBox(self.two_terminal_row ),HBox(self.four_terminal_row)] ,
                                layout=Layout(border='solid 1px',border_color='r',
                                              width='40%' )  )
        return results_box_wdgt
    
    def display_widgets_bar(self,num_terminals,num_modes):
        self.num_modes = num_modes
        self.num_terminals = num_terminals
        
        #horz_layout = Layout(dispaly='flex',flex_flow='row',overflow='scroll_hidden',width='70%')
        vert_layout = Layout(border='solid 1px',width='90%')
        horz_layout = Layout()
        display( VBox( [ HBox(self.chirality_wdgts[:self.num_modes+1],layout=horz_layout),
                        HBox(self.charge_wdgts[:self.num_modes+1],layout=horz_layout),
                        HBox(self.cent_charge_wdgts[:self.num_modes+1],layout=horz_layout) 
                       ] ,layout=vert_layout ) )
        

        display( VBox( [HBox(self.voltage_wdgts[:self.num_terminals+1] ), 
                        HBox(self.temperature_wdgts[:self.num_terminals+1]) ] ) , layout=vert_layout )

        self.take_widget_values()
        self.calculate_transport()
        
        # Display the conduction matrices
        display( HBox( [self.conduct_matrix_tabs(), self.conductance_results_box() ] )  )
        
        # Plot the Hall Bar
        self.qhbar = DrawQuantumHall( num_terminals = self.num_terminals, num_modes = self.num_modes,
                                chirality_vector = self.chirality_vector, charge_vector = self.charge_vector )
        self.qhbar.draw_bar()

        self.num_terminals_old, self.num_modes_old = self.num_terminals, self.num_modes
        #return voltage_wdgts

    
    def observe_widget_values(self):
        # observe quantum Hall quantities
        for mode in range(1, self.max_num_modes+1 ):
            self.chirality_wdgts[mode].observe( self.update_conductance_bar, names='value' )
            self.charge_wdgts[mode].observe( self.update_conductance_bar, names='value' )
            self.cent_charge_wdgts[mode].observe( self.update_conductance_bar, names='value' )
            
        
        # observe conduction coefficients
        for row in range(2,self.max_num_modes+2):
            for column in range(1,self.max_num_modes+1):
                self.conduct_matrix_wdgt_max['Charge'][row][column].observe( self.update_conductance_box, names='value' )
                self.conduct_matrix_wdgt_max['Heat'][row][column].observe( self.update_conductance_box, names='value' )
                
    def update_conductance_box(self,change):
        self.take_widget_values()
        self.calculate_transport()
        print('two terminal: ', self.two_terminal_electrical_conductance)
        self.two_terminal_row[1].value = '{:.2f}'.format(self.two_terminal_electrical_conductance)
        self.two_terminal_row[2].value = '{:.2f}'.format(self.two_terminal_thermal_conductance)
        self.four_terminal_row[1].value = '{:.2f}'.format(self.four_terminal_electrical_conductance)
        self.four_terminal_row[2].value = '{:.2f}'.format(self.four_terminal_thermal_conductance)

    def update_conductance_bar(self,change):
        self.qhbar.update_value('chirality_vector',self.chirality_vector)
        #print( self.qhbar.chirality_vector )
        self.qhbar.draw_bar()
        
        self.update_conductance_box(change)
        
    def display_all(self):
        #self.num_terminals_old, self.num_modes_old = 2,1
        self.max_num_modes = 10
        self.max_num_terminals = 12
        num_terminals_wdgt = widgets.BoundedIntText( value=self.num_terminals, 
                                                    min=2, max=self.max_num_terminals, step=1,
                                            description='Number of Terminals:', disabled=False,
                                            layout=Layout(width='200px'),style={'description_width': 'initial'})
        num_modes_wdgt = widgets.BoundedIntText( value=self.num_modes, 
                                                min=1, max=self.max_num_modes, step=1,
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
