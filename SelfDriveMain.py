from CarEnvironment import *
import os
import neat
import sys


def eval_genomes(genomes, config):
    global car, gene, net

    for genome_id, genome in genomes:
        car = pygame.sprite.GroupSingle(NEATCar())
        gene = genome
        net = neat.nn.FeedForwardNetwork.create(gene, config)
        gene.fitness = 0
        run = True
     
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            WINDOW.blit(TRACK, (0, 0))

            if car.sprite.alive == False:
                gene.fitness -=10
                break
           
            gene.fitness += 1
            outputs = net.activate(car.sprite.data())
            if outputs[0] > 0.7:
                car.sprite.direction = 1
            elif outputs[1] > 0.7:
                car.sprite.direction = -1
            else:
                car.sprite.direction = 0

            car.draw(WINDOW)
            car.update()
            pygame.display.update()
            

        #print(f"Genome {genome_id} evaluation complete. Final fitness: {gene.fitness}")

            
if __name__ == '__main__':
    global p
    local_dir = os.path.dirname(__file__) 
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(eval_genomes, 100)
    