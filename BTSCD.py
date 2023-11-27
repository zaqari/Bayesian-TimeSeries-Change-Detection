class cdm():

    def __init__(self,
                 y: np.ndarray,
                 time: None,
                 n_cat: int = 1,
                 samples: int = 1000,
                 chains: int = 1,
                 warm_up_rounds: int = 3000
                 ):
        super(cdm, self).__init__()

        data = {
            'y': y,
            'time': time,
            'n_cat': n_cat
        }

        # (1) Ensuring all requisite keys are in data-dictionary

        ## (1.1) removing any unused keys
        for k in list(data.keys()):
            if data[k] is None:
                del data[k]

        ## (1.2) ensuring that the length of the data is included
        data['n'] = len(data['y'])

        ## (1.3) ensuring that the number of categories is included
        if 'n_cat' not in data.keys():
            data['n_cat'] = 0

        ## (1.4) either creating t_max var if necessary, or deleting time var.
        if ('time' in data.keys()) and (data['n_cat'] > 1):
            data['t_max'] = data['time'].max()
        elif ('time' in data.keys()) and (data['n_cat'] <= 1):
            del data['time']


        # (2) Sampling distribution and returning poseriors
        self.posterior = None
        if data['n_cat'] > 1:
            self.posterior = self.__change_model(
                data=data,
                samples=samples,
                chains=chains,
                warm_up_rounds=warm_up_rounds
            )

        else:
            self.posterior = self.__null_model(
                data=data,
                samples=samples,
                chains=chains,
                warm_up_rounds=warm_up_rounds
            )


    def __change_model(self, data: dict, samples: int = 1000, chains: int = 1, warm_up_rounds: int = 3000):
        script = """
        model{
            gamma ~ dgamma(.001,.001)
            change_point[1] ~ dunif(0,.000001)
    
            for (i in 1:n_cat){
                change_point[i+1] ~ dunif(ifelse(i>1, change_point[i], 0), t_max)
                change_rate[i] ~ dnorm(0, .001)
            }
            
            for (j in 1:n){
                
                for (i in 1:n_cat){
                    theta[j,i] <- ifelse(time[j] >= change_point[i], change_rate[i], 0)
                } 
                mu[j] <- sum(theta[j,])
                y[j] ~ dnorm(mu[j], gamma)
                y_[j] ~ dnorm(mu[j], gamma)
            } 
            
        }
        """
        model = pyjags.Model(script, data=data, chains=chains, adapt=warm_up_rounds, progress_bar=True)
        return model.sample(samples, vars=['change_point', 'change_rate', 'y_'])


    def __null_model(self, data: dict,samples: int = 1000,chains: int=1,warm_up_rounds: int = 3000):
        script = """
        model{
            gamma ~ dgamma(.001,.001)
            change_rate ~ dnorm(0, .001)
            
            for (j in 1:n) {
                y[j] ~ dnorm(change_rate, gamma)
                y_[j] <- dnorm(change_rate, gamma)
            }
            
        }
        """

        model = pyjags.Model(script, data=data, chains=chains, adapt=warm_up_rounds, progress_bar=True)
        return model.sample(samples, vars=['change_rate', 'y_'])
