import numpy as np
import numpy.linalg as la

# in units of nanoAmp/microV
sigma0 = 3.87404e-5
kappa0 = 9.464298e-13

class QuantumHall:
    def __init__(self, chirality_vector=None,
                 charge_vector=None, charge_conduct_matrix=None,
                 central_charge_vector=None, heat_conduct_matrix=None,
                 num_terminals=None, inter_terminal_length_vector=None ,
                 voltages=None, temperatures = None
                 ):
        # size check

        # initializing

        # Default: all modes going downstream
        if chirality_vector is None:
            self.num_modes = 1
            self.chirality_vector = np.ones(self.num_modes, dtype=int)
        else:
            self.num_modes = len(chirality_vector)
            self.chirality_vector = chirality_vector

        # Default: all modes have charage 1
        if charge_vector is None:
            self.charge_vector = np.ones(self.num_modes, dtype=float)
        else:
            self.charge_vector = np.array(charge_vector,dtype=float)

        if charge_conduct_matrix is None:
            self.charge_conduct_matrix = np.zeros( (self.num_modes,self.num_modes),dtype=float )
        else:
            self.charge_conduct_matrix = np.matrix(charge_conduct_matrix,dtype=float)

        if central_charge_vector is None:
            self.central_charge_vector = np.ones(self.num_modes, dtype=float)
        else:
            self.central_charge_vector = np.array(central_charge_vector,dtype=float)

        if heat_conduct_matrix is None:
            self.heat_conduct_matrix = np.zeros( (self.num_modes,self.num_modes),dtype=float )
        else:
            self.heat_conduct_matrix = np.matrix(heat_conduct_matrix,dtype=float)

        if voltages is None and temperatures is None:
            if num_terminals is None:
                self.num_terminals = 4
            else:
                self.num_terminals =int( num_terminals )
            self.voltages = np.zeros(self.num_terminals, dtype=float)
            self.temperatures = np.zeros(self.num_terminals, dtype=float)
        elif voltages is None:
            self.num_terminals = len( temperatures )
            self.voltages = np.zeros(self.num_terminals, dtype=float)
            self.temperatures = np.array(temperatures)
        elif temperatures is None:
            self.num_terminals = len( voltages )
            self.voltages = np.array(voltages)
            self.temperatures = np.zeros(self.num_terminals, dtype=float)
        else:
            self.num_terminals = len( voltages )
            self.voltages = np.array(voltages)
            self.temperatures = np.array(temperatures)

        if inter_terminal_length_vector is None:
            self.inter_terminal_length_vector = np.ones(self.num_terminals, dtype=float)
        else:
            self.inter_terminal_length_vector = np.array(inter_terminal_length_vector,dtype=float)

        self._construct_d_propagation_matrix()

        self._conductance_tensor_calc_flag = { 'charge':False, 'heat':False  }

    def _construct_d_propagation_matrix(self):
        self.charge_d_propagation_matrix = np.matrix(
            [
                [ self.chirality_vector[b]/self.charge_vector[b]*(self.charge_conduct_matrix[a,b]-
            np.identity(self.num_modes)[a,b]*sum(self.charge_conduct_matrix[a,c]  for c in range(self.num_modes))  )
                                                         for a in range(self.num_modes)
                ]
                                                      for b in range(self.num_modes)
            ]
                                                       )

        self.heat_d_propagation_matrix = np.matrix(
            [
                [ self.chirality_vector[b]/self.central_charge_vector[b]*(self.heat_conduct_matrix[a,b]-
            np.identity(self.num_modes)[a,b]*sum(self.heat_conduct_matrix[a,c]  for c in range(self.num_modes))  )
                                                         for a in range(self.num_modes)
                ]
                                                      for b in range(self.num_modes)
            ]
                                                       )


    def _current_segment(self, d_propagation_matrix, potential_L,potential_R ,L):
        """
        Returns the two current (electrical or thermal):
        - that travels from the left terminal to the right one
        - that travels from the right terminal to the left one
        """

        eigvals , eigvecs = la.eig( np.matrix( d_propagation_matrix,dtype= np.float ) )

        # zero if positive and 1 if negative
        zeroone_vec = [ (1-c)/2 for c in self.chirality_vector  ]

        propagation_matrix = np.matrix( [ [np.exp( zeroone_vec[j]*L*eigvals[i]  )*eigvecs[j,i] for i in range(self.num_modes)]
                                          for j in range(self.num_modes)   ] ,dtype=np.double)

        emanating_currents =  np.array( [ (potential_L*(1+self.chirality_vector[i])/2 +
                                           potential_R*(-1+self.chirality_vector[i])/2 )*self.charge_vector[i] for i in range(self.num_modes) ] ,
                                            dtype=np.double)

        solution_coeffs = la.solve(propagation_matrix, emanating_currents)

        JLtoR = sum( sum( solution_coeffs[i]*eigvecs[j,i] for i in range(self.num_modes) ) for j in range(self.num_modes) )
        #JRtoL = sum( sum( solution_coeffs[i]*np.exp( eigvals[i]*L )*
         #                eigvecs[j,i] for i in range(self.num_modes) ) for j in range(self.num_modes) )

        return JLtoR



    def _electrical_current_all_terminals(self):
        current_outtoR = np.zeros(self.num_terminals)
        current_infromL = np.zeros(self.num_terminals)
        for segment in range(self.num_terminals):
            #current_LtoR[segment],current_RtoL[segment] =
            current = self.current_segment( self.charge_d_propagation_matrix, self.voltages[segment],
                                                                self.voltages[(segment+1)%self.num_terminals],
                                                                 self.inter_terminal_length_vector[segment] )
            current_outtoR[segment] = current
            current_infromL[ (segment+1)%self.num_terminals ] = current

        current_tot = np.zeros(self.num_terminals)
        #current_tot = []
        for terminal in range(self.num_terminals):
            current_tot[terminal] = -current_outtoR[terminal]+current_infromL[terminal]
            #current_tot.append( (current_infromL[terminal],current_outtoR[terminal]) )

        return current_tot

    def _electrical_current(self,terminal_1,terminal_2):
        current_tot = self._electrical_current_all_terminals()
        return current_tot[terminal_1]-current_tot[terminal_2]

    def conductance_tensor(self,quantity='charge'):
        """
        calculates sigma in
        - I = sigma.V for 'charge'
        - J = sigma.T^2/2 for 'heat'
        """
        if quantity=='charge':
            d_propagation_matrix = self.charge_d_propagation_matrix
            quant_charge_vector = self.charge_vector
        elif quantity=='heat':
            d_propagation_matrix = self.heat_d_propagation_matrix
            quant_charge_vector = self.central_charge_vector
        else:
            raise NotImplementedError("The argument quantity should be either 'charge' or 'heat' ")

        # zero if positive and 1 if negative
        zeroone_vec = [ (1-c)/2 for c in self.chirality_vector  ]

        d_plus = np.zeros( self.num_terminals, dtype=float )
        d_minus = np.zeros( self.num_terminals, dtype=float )

        eigvals , eigvecs = la.eig( np.matrix( d_propagation_matrix,dtype= np.float ) )
        #print( "eigs:  ",eigvals , eigvecs )
        for terminal in range(self.num_terminals):
            propagation_matrix = np.matrix( [ [np.exp( zeroone_vec[j]*self.inter_terminal_length_vector[terminal]*eigvals[a]  )
                                               *eigvecs[j,a] for a in range(self.num_modes)] 
                                             for j in range(self.num_modes)   ] ,dtype=np.float)
            #print( "prop: ", propagation_matrix )
            Ieig_Pinv = np.real( np.matmul( eigvecs,la.inv(propagation_matrix) ) )
            #print( Ieig_Pinv )
            d_plus[terminal] = sum( sum( Ieig_Pinv[j,i]*self.chirality_vector[i]*quant_charge_vector[i]*
                                        (1+self.chirality_vector[i] )/2 
                                        for j in range(self.num_modes)  )
                        for i in range(self.num_modes)  )
            d_minus[terminal] = sum( sum( Ieig_Pinv[j,i]*self.chirality_vector[i]*quant_charge_vector[i]*
                                         (1-self.chirality_vector[i] )/2 
                                         for j in range(self.num_modes)  )
                        for i in range(self.num_modes)  )
        #print( d_plus, d_minus )
        sigma = np.zeros( (self.num_terminals, self.num_terminals), dtype=float   )
        for terminal in range(self.num_terminals):
            sigma[terminal,(terminal-1 )%self.num_terminals ] += d_plus[ (terminal-1)%self.num_terminals ]
            sigma[terminal,terminal] = d_minus[ (terminal-1)%self.num_terminals ] - d_plus[terminal]
            sigma[terminal,(terminal+1 )%self.num_terminals ] += -d_minus[ terminal ]

        self._conductance_tensor_calc_flag[quantity]=True
        return sigma

    def _calc_conductance_tensors(self):
        self.charge_conductance_tensor = self.conductance_tensor('charge')
        self.heat_conductance_tensor = self.conductance_tensor('heat')

    def _temperature_to_heatcurrent(self, temperatures):
        return np.array( [ kappa0*temperatures[i]**2/2 for i in range( len(temperatures) ) ] )

    def current_all_terminals(self,quantity='charge',unit='quantized'):
        if unit=='quantized':
            unit_coeff = 1
        elif unit=='SI':
            unit_coeff = sigma0
        else:
            raise ValueError("The unit should be either 'quantized' or 'SI'")

        #self.calc_conductance_tensors()
        if quantity=='charge':
            self.charge_conductance_tensor = self.conductance_tensor('charge')
            # The unit of output electrical current will be in amperes
            return np.matmul( self.charge_conductance_tensor, self.voltages)*unit_coeff
        elif quantity=='heat':
            self.heat_conductance_tensor = self.conductance_tensor('heat')
            if unit=='quantized':
                return np.matmul( self.self.heat_conductance_tensor, self.temperatures)
            elif unit=='SI':
                # The unit of output electrical current will be in Watts
                return self._temperature_to_heatcurrent( np.matmul( self.heat_conductance_tensor, self.temperatures) )
        else:
            raise ValueError("The argument quantity should be either 'charge' or 'heat' ")

    def four_terminal_conductance( self ,current_terminals, potential_terminals ,quantity='charge'):
        if self.num_terminals <3:
            raise ValueError('Number of terminals shoud be at least 3')

        current_order = [ current_terminals[0]-1,current_terminals[1]-1 ]
        for terminal in range(self.num_terminals):
            if not(terminal+1 in current_terminals):
                current_order += [terminal]

        potential_order = [ potential_terminals[0]-1,potential_terminals[1]-1 ]
        for terminal in range(self.num_terminals):
            if not(terminal+1 in potential_terminals):
                potential_order += [terminal]

        if self._conductance_tensor_calc_flag[quantity]==False:
            if quantity=='charge':
                self.charge_conductance_tensor = self.conductance_tensor('charge')
            elif quantity=='heat':
                self.heat_conductance_tensor = self.conductance_tensor('heat')
            else:
                raise ValueError("The argument quantity should be either 'charge' or 'heat' ")


        if quantity=='charge':
            sigma_shuffled = self.charge_conductance_tensor[ current_order ].transpose()[potential_order].transpose()
        elif quantity=='heat':
            sigma_shuffled = self.heat_conductance_tensor[ current_order ].transpose()[potential_order].transpose()
        else:
            raise ValueError("The argument quantity should be either 'charge' or 'heat' ")

        sigma_SS = sigma_shuffled[:2,:2].copy()
        sigma_ST = sigma_shuffled[:2,2:self.num_terminals].copy()
        sigma_TS = sigma_shuffled[2:self.num_terminals,:2].copy()
        sigma_TT = sigma_shuffled[2:self.num_terminals,2:self.num_terminals].copy()
        #return self.charge_conductance_tensor, sigma_shuffled
        try:
            four_terminal_sigma = sigma_SS-np.matmul( sigma_ST, np.matmul( la.inv(sigma_TT ), sigma_TS) )
            return -four_terminal_sigma[0,0]
        except la.LinAlgError:
            raise la.LinAlgError( 'Error: The current between the terminals {} and {} cannot be determined from the potentials at'\
                  ' the terminals {} and {}'.format( current_terminals[0],current_terminals[1],potential_terminals[0],potential_terminals[1] ) )


    def two_terminal_conductance(self, voltage_terminals , quantity='charge'):
        if self.num_terminals>2:
            return self.four_terminal_conductance(voltage_terminals,voltage_terminals,quantity )

        if self._conductance_tensor_calc_flag[quantity]==False:
            if quantity=='charge':
                self.charge_conductance_tensor = self.conductance_tensor('charge')
            elif quantity=='heat':
                self.heat_conductance_tensor = self.conductance_tensor('heat')
            else:
                raise ValueError("The argument quantity should be either 'charge' or 'heat' ")

        if quantity=='charge':
            return -self.charge_conductance_tensor[0,0]
        elif quantity=='heat':
            return -self.heat_conductance_tensor[0,0]
        else:
            raise ValueError("The argument quantity should be either 'charge' or 'heat' ")
