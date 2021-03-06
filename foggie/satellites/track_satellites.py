#!/u/rcsimons/miniconda3/bin/python3.7
import astropy
from astropy.io import fits
from astropy.table import Table, Column
import numpy as np
from numpy import *
import math
from joblib import Parallel, delayed
import os, sys, argparse
import yt
from numpy import rec
from astropy.io import ascii
import foggie
from foggie.utils.foggie_utils import filter_particles
from foggie.utils.get_run_loc_etc import get_run_loc_etc
from foggie.utils.get_refine_box import get_refine_box
from foggie.utils.get_halo_center import get_halo_center
from foggie.utils.get_proper_box_size import get_proper_box_size
from foggie.utils import yt_fields
from foggie.satellites.make_satellite_projections import make_projection_plots
from yt.units import kpc


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='''identify satellites in FOGGIE simulations''')
    parser.add_argument('-system', '--system', metavar='system', type=str, action='store', \
                        help='Which system are you on? Default is Jase')
    parser.set_defaults(system="pleiades_raymond")

    parser.add_argument('--run', metavar='run', type=str, action='store',
                        help='which run? default is natural')
    parser.set_defaults(run="nref11c_nref9f")

    parser.add_argument('--halo', metavar='halo', type=str, action='store',
                        help='which halo? default is 8508 (Tempest)')
    parser.set_defaults(halo="8508")

    parser.add_argument('--pwd', dest='pwd', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)

    parser.add_argument('--run_all', dest='run_all', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)

    parser.add_argument('--do_sat_proj_plots', dest='do_sat_proj_plots', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)

    parser.add_argument('--do_proj_plots', dest='do_proj_plots', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)

    parser.add_argument('--do_sat_profiles', dest='do_sat_profiles', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)

    parser.add_argument('--do_measure_props', dest='do_measure_props', action='store_true',
                        help='just use the pwd?, default is no')
    parser.set_defaults(pwd=False)


    parser.add_argument('--output', metavar='output', type=str, action='store',
                        help='which output? default is RD0020')
    parser.set_defaults(output="DD0487")


    args = parser.parse_args()
    return args


def run_tracker(args, anchor_ids, sat, temp_outdir, id_all, x_all, y_all, z_all):
    print ('tracking %s %s'%(args.halo, sat))
    gd_indices = []
    print ('\t', args.halo, sat, 'finding anchor stars..')
    for a, anchor_id in enumerate(anchor_ids):
      match = where(id_all == anchor_id)[0]
      if len(match) > 0: gd_indices.append(int(match))

    x_anchors =  x_all[gd_indices]
    y_anchors =  y_all[gd_indices]
    z_anchors =  z_all[gd_indices]



    print (len(x_anchors))

   
    med_x = nanmedian(x_anchors).value
    med_y = nanmedian(y_anchors).value
    med_z = nanmedian(z_anchors).value







    if (not np.isnan(med_x)) & (len(gd_indices) > 500): 


          xbins = np.arange(med_x - 30, med_x+30, 0.05)
          ybins = np.arange(med_y - 30, med_y+30, 0.05)
          zbins = np.arange(med_z - 30, med_z+30, 0.05)

          gd = where((abs(x_anchors.value - med_x) < 30) & \
                     (abs(y_anchors.value - med_y) < 30) & \
                     (abs(z_anchors.value - med_z) < 30))


          x_anchors_use = x_anchors[gd].value
          y_anchors_use = y_anchors[gd].value
          z_anchors_use = z_anchors[gd].value

          stack_bins = (200, 200, 200)
          stack_positions = (x_anchors_use, y_anchors_use, z_anchors_use)

          H, edges = histogramdd(stack_positions, bins = stack_bins)
          argmax_H  = np.unravel_index(np.argmax(H, axis = None), H.shape)
          xedges = edges[0]
          yedges = edges[1]
          zedges = edges[2]
          x_sat = np.mean([xedges[argmax_H[0]],xedges[argmax_H[0]+1]]) 
          y_sat = np.mean([yedges[argmax_H[1]],yedges[argmax_H[1]+1]]) 
          z_sat = np.mean([zedges[argmax_H[2]],zedges[argmax_H[2]+1]]) 

    else:
          x_sat = np.nan
          y_sat = np.nan
          z_sat = np.nan
    print ('\t found location for %s %s: (%.3f, %.3f, %.3f)'%(args.halo, sat, x_sat, y_sat, z_sat))

    np.save(temp_outdir + '/' + args.halo + '_' + args.output + '_' + sat + '.npy', np.array([x_sat, y_sat, z_sat, len(gd_indices)]))

    return 

if __name__ == '__main__':
    args = parse_args()


    foggie_dir, output_dir, run_loc, trackname, haloname, spectra_dir, infofile = get_run_loc_etc(args)

    output_path = output_dir[0:output_dir.find('foggie')] + 'foggie'
    cat_dir = output_path + '/catalogs'
    fig_dir = output_path +  '/figures/track_satellites/%s'%args.halo
    temp_outdir = cat_dir + '/sat_track_locations/temp'

    if True:
      if not os.path.isdir(cat_dir): os.system('mkdir ' + cat_dir) 
      if not os.path.isdir(fig_dir): os.system('mkdir ' + fig_dir) 
      if not os.path.isdir(cat_dir + '/sat_track_locations'): os.system('mkdir ' + cat_dir + '/sat_track_locations')
      if not os.path.isdir(cat_dir + '/sat_track_locations/temp'): os.system('mkdir ' + cat_dir + '/sat_track_locations/temp')


      sat_cat = ascii.read(cat_dir + '/satellite_properties.cat')
      anchors = np.load(cat_dir + '/anchors.npy', allow_pickle = True)[()]
      anchors = anchors[args.halo]

      run_dir = foggie_dir + run_loc

      ds_loc = run_dir + args.output + "/" + args.output
      ds = yt.load(ds_loc)

      def _youngstars(pfilter, data):
            return data[(pfilter.filtered_type, "age")] < 2.e7 

      yt.add_particle_filter("youngstars",function=_youngstars, filtered_type='all',requires=["age"]) 
      ds.add_particle_filter('youngstars')

      track = Table.read(trackname, format='ascii')
      track.sort('col1')
      zsnap = ds.get_parameter('CosmologyCurrentRedshift')

      refine_box, refine_box_center, x_width = get_refine_box(ds, zsnap, track)

      small_sp = ds.sphere(refine_box_center, (20, 'kpc'))
      refine_box_bulk_vel = small_sp.quantities.bulk_velocity()
      all_data = ds.all_data()

      cond = not os.path.isfile('%s/%s/%s_%s.npy'%(temp_outdir.replace('/temp', ''), args.halo, args.halo, args.output))
      #cond = not os.path.isfile(temp_outdir + '/' + args.halo + '_' + args.output + '_0.npy')
      if False:
        load_particle_fields = ['particle_index',\
                                'particle_position_x', 'particle_position_y', 'particle_position_z']      

        filter_particles(all_data, load_particles = True, load_particle_types = ['stars'], load_particle_fields = load_particle_fields)

        print ('particles loaded')
        # Need to pass in these arrays, can't pass in refine box
        id_all = all_data['stars', 'particle_index']
        x_all  = all_data['stars', 'particle_position_x'].to('kpc')
        y_all  = all_data['stars', 'particle_position_y'].to('kpc')
        z_all  = all_data['stars', 'particle_position_z'].to('kpc')
    
        Parallel(n_jobs = -1)(delayed(run_tracker)(args, anchors[sat]['ids'], sat, temp_outdir, id_all, x_all, y_all, z_all) for sat in anchors.keys())

      else: 
        filter_particles(refine_box)



      output_fn = '%s/%s/%s_%s.npy'%(temp_outdir.replace('/temp', ''), args.halo, args.halo, args.output)
      if os.path.exists(output_fn):
        output = np.load('%s/%s/%s_%s.npy'%(temp_outdir.replace('/temp', ''), args.halo, args.halo, args.output), allow_pickle = True)[()]
        grid_prof_fields = [('deposit', 'youngstars_mass')]

        for sat in anchors.keys():
          if len(output[sat]['ray_den']) > 1:
            start = ds.arr([output[sat]['x'], output[sat]['y'], output[sat]['z']],  'kpc')
            sp_mass = ds.sphere(center = start, radius = 4*kpc)
            mass_prof = yt.create_profile(sp_mass, ['radius'], fields = grid_prof_fields, n_bins = 100, weight_field = None, accumulation = True)
            output[sat]['ystars_mass'] = mass_prof.field_data[('deposit', 'youngstars_mass')].to('Msun')
          else:
            output[sat]['ystars_mass'] = [np.nan]

        np.save('%s/%s/%s_%s.npy'%(temp_outdir.replace('/temp', ''), args.halo, args.halo, args.output), output)



      #Collect outputs   


      '''   
      output = {}
      annotate_others = []
      all_start_arrows = []
      all_end_arrows = []

      for sat in anchors.keys():
        temp = np.load(temp_outdir + '/' + args.halo + '_' + args.output + '_' + sat + '.npy')
        output[sat] = {}
        output[sat]['number_stars'] = int(temp[3])
        output[sat]['x_init'] = round(temp[0], 3)
        output[sat]['y_init'] = round(temp[1], 3)
        output[sat]['z_init'] = round(temp[2], 3)

        if np.isnan(temp[0]): 

          output[sat]['x'] = np.nan
          output[sat]['y'] = np.nan
          output[sat]['z'] = np.nan

          output[sat]['vx'] = np.nan
          output[sat]['vy'] = np.nan
          output[sat]['vz'] = np.nan

          output[sat]['ray_den'] = [np.nan]
          output[sat]['ray_vel'] = [np.nan]
          output[sat]['ray_dist'] = [np.nan]
          output[sat]['mass_dist'] = [np.nan]
          output[sat]['gas_mass'] = [np.nan]
          output[sat]['dm_mass'] = [np.nan]
          output[sat]['stars_mass'] = [np.nan]
          output[sat]['cold_mass_dist'] = [np.nan]
          output[sat]['cold_gas_mass'] = [np.nan]


          continue


        sp = ds.sphere(center = ds.arr(temp[0:3], 'kpc'), radius = 1*kpc)
  
        com = sp.quantities.center_of_mass(use_gas=False, use_particles=True, particle_type = 'stars').to('kpc')

        com_x = float(com[0].value)
        com_y = float(com[1].value)
        com_z = float(com[2].value)

        output[sat]['x'] = round(com_x, 3)
        output[sat]['y'] = round(com_y, 3)
        output[sat]['z'] = round(com_z, 3)

        stars_vx = sp.quantities.weighted_average_quantity(('stars', 'particle_velocity_x'), ('stars', 'particle_mass')).to('km/s')
        stars_vy = sp.quantities.weighted_average_quantity(('stars', 'particle_velocity_y'), ('stars', 'particle_mass')).to('km/s')
        stars_vz = sp.quantities.weighted_average_quantity(('stars', 'particle_velocity_z'), ('stars', 'particle_mass')).to('km/s')

        output[sat]['vx'] = round(float(stars_vx.value), 3)
        output[sat]['vy'] = round(float(stars_vy.value), 3)
        output[sat]['vz'] = round(float(stars_vz.value), 3)

        start = ds.arr([com_x, com_y, com_z],  'kpc')

        
        vel = ds.arr([stars_vx, stars_vy, stars_vz], 'km/s')
        vel_norm= vel / np.sqrt(sum(vel**2.))
        
        disk = ds.disk(center = start + 2.5 * vel_norm * kpc, normal = vel_norm, radius = 0.5*kpc, height = 2.5*kpc)

        
        disk.set_field_parameter('center', start.to('code_length'))
        disk.set_field_parameter('bulk_velocity', vel.to('code_velocity'))

        grid_prof_fields = [('gas', 'cell_mass'), \
                            ('deposit', 'stars_mass'), \
                            ('deposit', 'youngstars_mass'), \
                            ('deposit', 'dm_mass')]

        sp_mass = ds.sphere(center = start, radius = 4*kpc)
        sp_mass_cold = sp_mass.cut_region(["(obj['temperature'] < {} )".format(1.5e4)])
        if len(disk["index", "cylindrical_z"]) > 2:
             profiles = yt.create_profile(disk, ("index", "cylindrical_z"), [("gas", "density"), ('gas', 'velocity_cylindrical_z')], weight_field = ('index', 'cell_volume')) 
             mass_prof = yt.create_profile(sp_mass, ['radius'], fields = grid_prof_fields, n_bins = 100, weight_field = None, accumulation = True)
             cold_mass_prof = yt.create_profile(sp_mass_cold, ['radius'], fields = [('gas', 'cell_mass')], n_bins = 100, weight_field = None, accumulation = True)


             output[sat]['ray_den'] = profiles.field_data[("gas", "density")].to('g/cm**3.')
             output[sat]['ray_vel'] = profiles.field_data[('gas', 'velocity_cylindrical_z')].to('km/s')
             output[sat]['ray_dist'] = profiles.x.to('kpc')
             output[sat]['mass_dist'] = mass_prof.x.to('kpc')
             output[sat]['gas_mass'] = mass_prof.field_data[('gas', 'cell_mass')].to('Msun')
             output[sat]['dm_mass'] = mass_prof.field_data[('deposit', 'dm_mass')].to('Msun')
             output[sat]['stars_mass'] = mass_prof.field_data[('deposit', 'stars_mass')].to('Msun')
             output[sat]['ystars_mass'] = mass_prof.field_data[('deposit', 'youngstars_mass')].to('Msun')
             output[sat]['cold_mass_dist'] = cold_mass_prof.x.to('kpc')
             output[sat]['cold_gas_mass'] = cold_mass_prof.field_data[('gas', 'cell_mass')].to('Msun')


        else:
             output[sat]['ray_den'] = [np.nan]
             output[sat]['ray_vel'] = [np.nan]
             output[sat]['ray_dist'] = [np.nan]
             output[sat]['mass_dist'] = [np.nan]
             output[sat]['gas_mass'] = [np.nan]
             output[sat]['dm_mass'] = [np.nan]
             output[sat]['stars_mass'] = [np.nan]
             output[sat]['ystars_mass'] = [np.nan]
             output[sat]['cold_mass_dist'] = [np.nan]
             output[sat]['cold_gas_mass'] = [np.nan]



        point_sat = ds.point(start)
        overlap = point_sat & refine_box
        
        output[sat]['in_refine_box'] = overlap.sum("cell_volume") > 0
        print (output[sat]['in_refine_box'])

        fig_width = 10 * kpc
        start_arrow = start
        vel_fixed = vel - refine_box_bulk_vel
        vel_fixed_norm = vel_fixed / ds.arr(200, 'km/s')

        end_arrow = start + vel_fixed_norm * ds.arr(1, 'kpc')

        if np.isnan(com_x): start_use = ds.arr(temp, 'kpc')
        else: start_use = start

        make_projection_plots(all_data.ds, start_use, all_data, fig_width, fig_dir, haloname, \
                            fig_end = 'satellite_{}_{}'.format(args.output, sat), \
                            do = ['gas', 'stars'], axes = ['x'],  annotate_positions = [start],\
                            add_arrow = True, start_arrow = [start_arrow], end_arrow = [end_arrow])

        if output[sat]['in_refine_box']:
          annotate_others.append(ds.arr([output[sat]['x'], output[sat]['y'], output[sat]['z']], 'kpc'))
          all_start_arrows.append(start_arrow)
          end_arrow = start + vel_fixed_norm * ds.arr(5, 'kpc')
          all_end_arrows.append(end_arrow)


      make_projection_plots(refine_box.ds, ds.arr(refine_box_center, 'code_length').to('kpc'),\
                            refine_box, x_width, fig_dir, haloname,\
                            fig_end = 'box_center_{}'.format(args.output),\
                            do = ['gas', 'stars'], axes = ['x'],\
                            annotate_positions = annotate_others, is_central = True, add_arrow = True,\
                            start_arrow = all_start_arrows, end_arrow = all_end_arrows)



      np.save('%s/%s/%s_%s.npy'%(temp_outdir.replace('/temp', ''), args.halo, args.halo, args.output), output)
      os.system('rm %s/%s_%s_*.npy'%(temp_outdir, args.halo, args.output))
      '''
